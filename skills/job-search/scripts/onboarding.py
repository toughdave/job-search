#!/usr/bin/env python3
"""Project-scoped interview coverage derived from saved evidence, never checkboxes."""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import workspace as ws

def baseline_topics():
    return [
        {'id':'region','track_id':None,'kind':'profile','title':'Search location and constraints','required':True,'dimensions':['location','constraints']},
        {'id':'background','track_id':None,'kind':'profile','title':'Work, projects and education','required':True,'dimensions':['roles','education']},
        {'id':'linkedin','track_id':None,'kind':'linkedin','title':'Optional LinkedIn review choice','required':True,'dimensions':['decision']},
        {'id':'contact-name','track_id':None,'kind':'profile','title':'Name to use on applications','required':True,'dimensions':['name']},
        {'id':'contact-email','track_id':None,'kind':'profile','title':'Application email address','required':True,'dimensions':['email']},
        {'id':'contact-phone','track_id':None,'kind':'profile','title':'Application phone number','required':True,'dimensions':['phone']},
        {'id':'credentials','track_id':None,'kind':'profile','title':'Certifications and professional licences','required':True,'dimensions':['certifications']},
        {'id':'relocation','track_id':None,'kind':'profile','title':'Willingness to relocate and any limits','required':True,'dimensions':['relocation']}
    ]

def validate(state, root):
    ob=state.get('onboarding')
    if ob is None: return  # Read older workspaces without destructive migration.
    ws.require(isinstance(ob,dict) and ob.get('version')==1,'Unsupported onboarding format.')
    ws.require(ob.get('workspace_id')==state['workspace_id'],'Onboarding belongs to a different workspace.')
    project=ws.checked_root(ob.get('project_root',''))
    ws.require(str(project)==ob.get('project_root') and project.is_dir(),'Onboarding project path is missing or noncanonical.')
    sources=ws.indexed(state['sources'],'sources');facts=ws.indexed(state['profile']['facts'],'facts')
    answers=ws.indexed(state['interviews'],'interviews')
    tracks=ws.indexed(ob.get('tracks'),'tracks');topics=ws.indexed(ob.get('topics'),'topics')
    for expected in baseline_topics():
        topic=topics.get(expected['id'])
        if topic is not None:
            ws.require(topic.get('required') is True and topic.get('track_id') is None and topic.get('kind')==expected['kind'] and set(expected['dimensions']).issubset(topic.get('dimensions',[])),'Baseline profile coverage cannot be disabled.')
    ws.require(ob.get('active_track') is None or ob['active_track'] in tracks,'Unknown active occupation.')
    for track in tracks.values():
        ws.require(isinstance(track.get('occupation'),str) and track['occupation'].strip(),'Occupation label required.')
        ws.refs(track.get('source_ids'),sources,'Occupation')
    for topic in topics.values():
        ws.require(topic.get('track_id') is None or topic['track_id'] in tracks,'Topic occupation mismatch.')
        ws.require(topic.get('kind') in ('profile','example','linkedin'),'Unknown interview topic kind.')
        ws.require(isinstance(topic.get('title'),str) and topic['title'].strip(),'Topic title required.')
        dims=topic.get('dimensions')
        ws.require(isinstance(dims,list) and dims and all(isinstance(x,str) and x for x in dims) and len(dims)==len(set(dims)),'Distinct topic dimensions required.')
        if topic['kind']=='example':
            ws.require({'context','personal_action','tools','result'}.issubset(dims),'Example topics need context, personal action, tools/methods and result.')
        ws.require(isinstance(topic.get('required'),bool),'Topic required flag must be explicit.')
    questions=ws.indexed(ob.get('questions'),'questions')
    for q in questions.values():
        ws.require(q.get('topic_id') in topics and q.get('dimension') in topics[q['topic_id']]['dimensions'],'Question topic/dimension mismatch.')
        ws.require(isinstance(q.get('question'),str) and q['question'].strip(),'Exact pending question required.')
        ws.stamp(q.get('asked_at'),'question asked_at')
    for answer in answers.values():
        qid=answer.get('onboarding_question_id')
        if qid is not None:
            ws.require(qid in questions and answer['question']==questions[qid]['question'],'Answer must match its saved onboarding question.')
    for ev in ws.indexed(ob.get('evidence'),'interview evidence').values():
        ws.require(ev.get('topic_id') in topics and ev.get('dimension') in topics[ev['topic_id']]['dimensions'],'Evidence topic/dimension mismatch.')
        ws.refs(ev.get('source_ids'),sources,'Interview evidence')
        ids=ev.get('fact_ids');ws.require(isinstance(ids,list) and ids and all(x in facts for x in ids),'Evidence needs known fact IDs.')
        ws.require(all(set(facts[x]['source_ids']).intersection(ev['source_ids']) for x in ids),'Evidence sources must support the linked facts.')
        ws.require(isinstance(ev.get('rationale'),str) and ev['rationale'].strip(),'Explain how the evidence answers this dimension.')
        ws.refs(ev.get('answer_ids',[]),answers,'Evidence answers',False)
    for choice in ws.indexed(ob.get('dispositions'),'topic dispositions').values():
        ws.require(choice.get('topic_id') in topics,'Disposition topic missing.')
        ws.require(choice.get('status') in ('declined','deferred','not_applicable','no_example','reopen'),'Invalid topic disposition.')
        ws.refs(choice.get('source_ids'),sources,'Disposition')
        ws.require(any(sources[x]['kind'] in ('candidate_answer','candidate_report') for x in choice['source_ids']),'Skipping/reopening needs the candidate decision.')
        ws.require(isinstance(choice.get('reason'),str) and choice['reason'].strip(),'Disposition reason required.')
    intake=ob.get('resume');ws.require(isinstance(intake,dict),'Resume intake record required.')
    ws.require(intake.get('status') in ('unchecked','awaiting_file','unreadable','read','no_resume'),'Invalid resume intake status.')
    ws.refs(intake.get('source_ids',[]),sources,'Resume intake',intake['status']!='unchecked')
    if intake['status']=='read':
        ws.require(any(sources[x]['kind']=='resume' for x in intake['source_ids']),'Resume read requires a saved resume source.')
        tid=intake.get('text_source_id');ws.require(tid in sources and tid in intake['source_ids'],'Readable resume text source required.')
        p=ws.inside(root,sources[tid]['file'])
        ws.require(p.suffix.lower() in ('.txt','.md') and p.read_text(encoding='utf-8').strip(),'Resume text must be saved and nonempty.')
    if intake['status']=='no_resume':
        ws.require(any(sources[x]['kind'] in ('candidate_answer','candidate_report') for x in intake['source_ids']),'No-resume route requires the candidate answer.')
    import experience
    experience.validate(state)

def guard_history(old,new):
    before=old.get('onboarding');after=new.get('onboarding')
    if before is None:return
    ws.require(after is not None,'Saved onboarding cannot be deleted.')
    for key in ('version','workspace_id','project_root'):
        ws.require(after.get(key)==before[key],'Cannot silently rebind the interview to another project.')
    for key in ('tracks','topics','questions','evidence','dispositions','experiences','history_reviews'):
        ws.require(after.get(key,[])[:len(before.get(key,[]))]==before.get(key,[]),f'Onboarding {key} order is append-only.')
        previous=ws.indexed(before.get(key,[]),key);current=ws.indexed(after.get(key,[]),key)
        ws.require(all(k in current and current[k]==v for k,v in previous.items()),f'Onboarding {key} is append-only.')

def bind(value,project_value):
    root=ws.checked_root(value);project=ws.checked_root(project_value)
    ws.require(project.is_dir(),'Choose an existing project folder.')
    ws.require(not (project/'SKILL.md').exists(),'An installed skill cannot be the candidate project.')
    state=ws.load(root)
    if state.get('onboarding'):
        check_project(state,project);return state
    state['onboarding']={'version':1,'workspace_id':state['workspace_id'],'project_root':str(project),
        'resume':{'status':'unchecked','source_ids':[]},'tracks':[],'active_track':None,
        'topics':baseline_topics(),'questions':[],'evidence':[],'dispositions':[],'experiences':[],'history_reviews':[]}
    return ws.commit(root,state,state['revision'],'Bound private interview to the selected project')

def check_project(state,project):
    ws.require(state.get('onboarding') is not None,'Bind this workspace to the selected project first.')
    ws.require(str(ws.checked_root(project))==state['onboarding']['project_root'],'Different project: do not reuse this interview or its private evidence automatically.')

def plan(value,project):
    state=ws.load(value);check_project(state,project);ob=state['onboarding']
    facts={x['id']:x for x in state['profile']['facts']}
    current=lambda ids: all(facts[x]['status'] in ('candidate_reported','verified') for x in ids)
    answers={q['onboarding_question_id']:q for q in state['interviews'] if q.get('onboarding_question_id')}
    dispositions={x['topic_id']:x for x in ob['dispositions']}
    replaced={e['supersedes'] for e in ob.get('experiences',[]) if e.get('supersedes')}
    rows=[]
    for topic in ob['topics']:
        if topic['track_id'] not in (None,ob['active_track']):continue
        if topic.get('experience_id') in replaced:continue
        evidence=[e for e in ob['evidence'] if e['topic_id']==topic['id'] and current(e['fact_ids'])]
        covered={e['dimension'] for e in evidence}
        missing=[d for d in topic['dimensions'] if d not in covered]
        choice=dispositions.get(topic['id']);disposition=choice['status'] if choice else None
        if disposition=='reopen':disposition=None
        status=disposition or ('answered' if not missing else 'partial' if covered else 'unanswered')
        pending=[];unmapped=[]
        for q in ob['questions']:
            if q['topic_id']!=topic['id'] or q['dimension'] not in missing:continue
            if q['id'] in answers:unmapped.append(answers[q['id']]['id'])
            elif not disposition:pending.append(q)
        rows.append({'id':topic['id'],'title':topic['title'],'experience_id':topic.get('experience_id'),'status':status,'checked':status=='answered',
            'required':topic['required'],'missing_dimensions':missing,'pending_questions':pending,
            'unmapped_answer_ids':unmapped,'review_saved_evidence_before_asking':bool(missing and not disposition),
            'fact_ids':sorted({x for e in evidence for x in e['fact_ids']})})
    # Never conclude onboarding is complete merely because no topics were configured.
    active=ob['active_track'];required=[r for r in rows if r['required']]
    has_examples=any(t['track_id']==active and t['kind']=='example' and t['required'] for t in ob['topics']) if active else False
    unresolved=[r['id'] for r in required if r['status'] not in ('answered','declined','not_applicable','no_example')]
    import experience
    history=experience.coverage(state,rows)
    configured={t['id']:t for t in ob['topics']}
    missing_baseline=[t for t in baseline_topics() if t['id'] not in configured]
    return {'workspace_id':state['workspace_id'],'revision':state['revision'],'project_root':ob['project_root'],
        'active_track':active,'resume_status':ob['resume']['status'],'topics':rows,
        'work_history':history,
        'missing_baseline_topics':missing_baseline,
        'ready_to_close_interview':bool(active and has_examples and required and ob['resume']['status'] in ('read','no_resume') and not unresolved and history['ready'] and not missing_baseline),
        'unresolved_required_topics':unresolved,
        'instruction':'Review all existing facts and exact answers for each missing dimension before asking. Map supported answers into evidence; do not repeat an answered question. Checked is derived, never an input.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('bind','plan'))
    parser.add_argument('--workspace',required=True);parser.add_argument('--project',required=True);args=parser.parse_args()
    try:
        result=bind(args.workspace,args.project) if args.command=='bind' else plan(args.workspace,args.project)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError) as e:
        print(f'Onboarding error: {e}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
