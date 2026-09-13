#!/usr/bin/env python3
"""Project-scoped interview coverage derived from saved evidence, never checkboxes."""
import argparse
import json
import re
import uuid
from pathlib import Path,PureWindowsPath,PurePosixPath
import sys
sys.dont_write_bytecode = True
import workspace as ws

def absolute_path(value):
    return isinstance(value,str) and (PureWindowsPath(value).is_absolute() or PurePosixPath(value).is_absolute())

def baseline_topics():
    return [
        {'id':'target-work','track_id':None,'kind':'profile','title':'Work the candidate wants to find','required':True,'dimensions':['occupation']},
        {'id':'region','track_id':None,'kind':'profile','title':'Search location and constraints','required':True,'dimensions':['location','constraints']},
        {'id':'background','track_id':None,'kind':'profile','title':'Work, projects and education','required':True,'dimensions':['roles','education']},
        {'id':'linkedin','track_id':None,'kind':'linkedin','title':'Optional LinkedIn review choice','required':True,'dimensions':['decision']},
        {'id':'contact-name','track_id':None,'kind':'profile','title':'Name to use on applications','required':True,'dimensions':['name']},
        {'id':'contact-email','track_id':None,'kind':'profile','title':'Application email address','required':True,'dimensions':['email']},
        {'id':'contact-phone','track_id':None,'kind':'profile','title':'Application phone number','required':True,'dimensions':['phone']},
        {'id':'credentials','track_id':None,'kind':'profile','title':'Certifications and professional licences','required':True,'dimensions':['certifications']},
        {'id':'relocation','track_id':None,'kind':'profile','title':'Willingness to relocate and any limits','required':True,'dimensions':['relocation']},
        {'id':'routine-choice','track_id':None,'kind':'profile','title':'Optional weekday morning search','required':True,'dimensions':['decision']},
        {'id':'linkedin-url','track_id':None,'kind':'profile','title':'LinkedIn profile link for resume or explicit omission','required':True,'dimensions':['url']},
        {'id':'resume-format','track_id':None,'kind':'profile','title':'Approve resume/CV length after reviewing history and destination','required':True,'dimensions':['decision']}
    ]

def validate(state, root):
    ob=state.get('onboarding')
    if ob is None: return  # Read older workspaces without destructive migration.
    ws.require(isinstance(ob,dict) and ob.get('version')==1,'Unsupported onboarding format.')
    ws.require(ob.get('workspace_id')==state['workspace_id'],'Onboarding belongs to a different workspace.')
    project=ob.get('project_root')
    ws.require(absolute_path(project),'Onboarding project must be an absolute path.')
    sources=ws.indexed(state['sources'],'sources');facts=ws.indexed(state['profile']['facts'],'facts')
    for binding in ob.get('bindings',[]):
        ws.require(isinstance(binding,dict) and all(absolute_path(binding.get(k)) for k in ('from','to')),'Binding history paths required.')
        ws.stamp(binding.get('at'),'binding timestamp')
        ws.refs(binding.get('source_ids'),sources,'Binding decision')
        ws.require(any(sources[x]['kind'] in ('candidate_answer','candidate_report') for x in binding['source_ids']),'Rebinding needs a saved candidate decision.')
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

def guard_history(old,new,allow_rebind=False):
    before=old.get('onboarding');after=new.get('onboarding')
    if before is None:return
    ws.require(after is not None,'Saved onboarding cannot be deleted.')
    for key in ('version','workspace_id'):
        ws.require(after.get(key)==before[key],'Cannot silently rebind the interview to another project.')
    previous=before.get('bindings',[]);current=after.get('bindings',[])
    ws.require(current[:len(previous)]==previous,'Binding history is append-only.')
    if after['project_root']!=before['project_root'] or current!=previous:
        ws.require(allow_rebind and len(current)==len(previous)+1,'Use the explicit rebind command for a project move.')
        ws.require(current[-1]['from']==before['project_root'] and current[-1]['to']==after['project_root'],'Binding history must describe this move.')
    for key in ('tracks','topics','questions','evidence','dispositions','experiences','history_reviews'):
        ws.require(after.get(key,[])[:len(before.get(key,[]))]==before.get(key,[]),f'Onboarding {key} order is append-only.')
        previous=ws.indexed(before.get(key,[]),key);current=ws.indexed(after.get(key,[]),key)
        ws.require(all(k in current and current[k]==v for k,v in previous.items()),f'Onboarding {key} is append-only.')
    import experience
    experience.guard_reviews(old,new)

POINTER='.job-search-project.json'

def pointer_path(project,state):
    ws.require(not (project/'SKILL.md').exists() and not (project/'skills/job-search/SKILL.md').exists(),'An installed skill/public skill checkout cannot be the candidate project.')
    path=ws.inside(project,POINTER)
    if path.exists():
        existing=json.loads(path.read_text(encoding='utf-8'))
        ws.require(existing.get('format')=='job-search-project' and existing.get('workspace_id')==state['workspace_id'],'Project already points to a different workspace; no pointer overwritten.')
    return path

def write_pointer(root,project,state):
    path=pointer_path(project,state)
    relative=root.relative_to(project).as_posix() if root.is_relative_to(project) else None
    ws.atomic_json(path,{'format':'job-search-project','workspace_id':state['workspace_id'],
        'workspace_path':str(root),'workspace_relative':relative,
        'instruction':'Read this workspace from disk; verify its workspace ID. If the project moved, ask for the new binding before continuing.'})

def bind(value,project_value):
    root=ws.checked_root(value);project=ws.checked_root(project_value)
    ws.require(project.is_dir(),'Choose an existing project folder.')
    state=ws.load(root)
    pointer_path(project,state)
    if state.get('onboarding'):
        check_project(state,project);write_pointer(root,project,state);return state
    state['onboarding']={'version':1,'workspace_id':state['workspace_id'],'project_root':str(project),
        'resume':{'status':'unchecked','source_ids':[]},'tracks':[],'active_track':None,
        'topics':baseline_topics(),'questions':[],'evidence':[],'dispositions':[],'experiences':[],'history_reviews':[]}
    state=ws.commit(root,state,state['revision'],'Bound private interview to the selected project')
    write_pointer(root,project,state)
    return state

def rebind(value,project_value,source_id,expected,workspace_id):
    root=ws.checked_root(value);project=ws.checked_root(project_value);state=ws.load(root)
    ws.require(state['workspace_id']==workspace_id,'Confirm the original workspace ID before rebinding.')
    ws.require(state['revision']==expected,'Revision conflict: reread before rebinding.')
    ws.require(project.is_dir() and state.get('onboarding'),'Existing project and bound workspace required.')
    pointer_path(project,state)
    sources=ws.indexed(state['sources'],'sources')
    ws.require(source_id in sources and sources[source_id]['kind'] in ('candidate_answer','candidate_report'),'Save the candidate relocation decision before rebinding.')
    ob=state['onboarding'];previous=ob['project_root']
    ob.setdefault('bindings',[]).append({'from':previous,'to':str(project),'at':ws.now(),'source_ids':[source_id]})
    ob['project_root']=str(project)
    # A timer may still carry the old project or workspace path. Require native readback again.
    routine=state['integrations'].get('job_search_routine')
    if routine and routine.get('status')=='active':routine['status']='paused'
    state=ws.commit(root,state,expected,'Candidate-directed project relocation; recheck schedule paths',allow_rebind=True)
    write_pointer(root,project,state)
    return state

def check_project(state,project):
    ws.require(state.get('onboarding') is not None,'Bind this workspace to the selected project first.')
    actual=ws.checked_root(project);saved=Path(state['onboarding']['project_root'])
    ws.require(actual.is_dir() and saved.is_dir(),'Project moved or is unavailable. Read records with workspace.py show; confirm the new location and use onboarding.py rebind.')
    ws.require(ws.same_path(actual,saved),'Different project: do not reuse this interview or its private evidence automatically. A confirmed move uses onboarding.py rebind.')

def ask(value,project,topic_id,dimension,question,expected):
    root=ws.checked_root(value);state=ws.load(root);check_project(state,project)
    ws.require(state['revision']==expected,'Revision conflict: reread before asking.')
    review=plan(root,project)
    pending=[q for row in review['topics'] for q in row['pending_questions']]
    if pending:
        ws.require(len(pending)==1 and pending[0]['topic_id']==topic_id and pending[0]['dimension']==dimension and pending[0]['question']==question,'Resume the existing pending question before asking another.')
        if state['session']['next_action']!='Await answer: '+question:
            state['session']['next_action']='Await answer: '+question
            state=ws.commit(root,state,expected,'Restored saved pending question as the next action')
        return {'question':pending[0],'revision':state['revision']}
    ws.require(not any(row['unmapped_answer_ids'] for row in review['topics'] if row['status'] not in ('declined','deferred','not_applicable','no_example')),'Reconcile saved unmapped answers before asking another question.')
    for topic in review['missing_baseline_topics']:state['onboarding']['topics'].append(topic)
    row=next((r for r in review['topics'] if r['id']==topic_id),None)
    ws.require(row is None or (row['status'] not in ('declined','deferred','not_applicable','no_example') and dimension in row['missing_dimensions']),'Topic is covered or has a saved disposition; reconcile it first.')
    ws.require(question.count('?')+question.count('？')<=1,'Ask one question; split multiple decisions into separate turns.')
    if topic_id in ('contact-name','contact-email','contact-phone'):
        contact_fields=[bool(re.search(pattern,question,re.I)) for pattern in (r'\bname\b',r'\be-?mail\b',r'\b(?:phone|telephone|mobile)\b')]
        ws.require(sum(contact_fields)<=1,'Ask for one contact field per turn: name, email and phone are separate topics.')
    interrogative=r'(?:what|where|when|why|how|which|who|whose|(?:do|does|did|are|is|can|could|would|will|have|has)\s+you)\b'
    clauses=re.split(r'(?:\b(?:and|or|also|plus)\s+|;\s*)',question,flags=re.I)
    alternatives=re.split(r'\bor\s+',question,flags=re.I)
    choice=False
    if len(alternatives)==2:
        first,second=(part.strip() for part in alternatives)
        polar=bool(re.match(r'(?:would|do|are|can|could|will|should)\b',first,re.I))
        preference=bool(re.match(r'(?:would you (?:rather|prefer)|do you (?:want|prefer)|should I)\b',second,re.I))
        verb=lambda part:re.match(r'(?:do|are|would|can|could|will|should)\s+(?:you|I)\s+\w+',part,re.I)
        left,right=verb(first),verb(second)
        shared=bool(left and right and left.group().casefold()==right.group().casefold())
        choice=polar and (preference or shared)
    ws.require(choice or not (len(clauses)>1 and re.search(interrogative,clauses[0],re.I)
                    and any(re.match(interrogative,part,re.I) for part in clauses[1:])),
               'This appears to combine separate questions. Ask one decision now and save the other for a later turn.')
    if topic_id=='linkedin':
        ws.require(not (re.search(r'\b(?:link|url|address)\b',question,re.I)
                        and not re.search(r'\b(?:review|improve|update|audit|feedback)\b',question,re.I)),
                   'Profile URL/inclusion belongs to topic linkedin-url, dimension url. Topic linkedin is the optional profile review decision.')
    q={'id':'q-'+uuid.uuid4().hex,'topic_id':topic_id,'dimension':dimension,'question':question,'asked_at':ws.now()}
    state['onboarding']['questions'].append(q);state['session']['next_action']='Await answer: '+question
    saved=ws.commit(root,state,expected,'Saved the next interview question')
    return {'question':q,'revision':saved['revision']}

def save_answer(value,project,question_id,answer,interpretation,expected):
    root=ws.checked_root(value);state=ws.load(root);check_project(state,project)
    ws.require(state['revision']==expected,'Revision conflict: reread before saving the answer.')
    q=next((q for q in state['onboarding']['questions'] if q['id']==question_id),None)
    ws.require(q is not None,'Unknown pending question.')
    existing=next((a for a in state['interviews'] if a.get('onboarding_question_id')==question_id),None)
    if existing:
        ws.require(existing['answer']==answer and existing['interpretation']==interpretation,'Answer already saved; append a sourced correction rather than overwrite it.')
        return {'answer':existing,'revision':state['revision'],'captured_characters':len(answer)}
    ws.require(answer.strip() and interpretation.strip(),'Exact answer and a separate interpretation are required.')
    sid='answer-'+uuid.uuid4().hex;relative='sources/'+sid+'.json'
    path=ws.inside(root,relative)
    with path.open('x',encoding='utf-8') as f:json.dump({'question':q['question'],'answer':answer},f,ensure_ascii=False,indent=2)
    source={'id':sid,'kind':'candidate_answer','recorded_at':ws.now(),'file':relative,'sha256':ws.digest(path)}
    a={'id':sid,'onboarding_question_id':q['id'],'question':q['question'],'answer':answer,'interpretation':interpretation,'recorded_at':ws.now(),'source_ids':[sid]}
    state['sources'].append(source);state['interviews'].append(a)
    state['session']['next_action']='Reconcile saved answer '+sid+' into supported facts and topic evidence before the next question.'
    saved=ws.commit(root,state,expected,'Saved exact candidate answer; coverage awaits reconciliation')
    return {'answer':a,'revision':saved['revision'],'captured_characters':len(answer),
            'capture_instruction':'Compare this saved answer with the full received message, including pasted postings and extra details. A saved file alone cannot prove the composer message was copied completely.'}


CAPTURE_INSTRUCTION = 'Compare the saved text and character count with the ENTIRE received message, including requests, pasted postings and extra details. Additional employer-source copies do not replace the original message. This helper cannot see text omitted by the caller.'


def check_reply(value,project,reply,expected):
    """Read-only check of the actual proposed interview reply, not a question summary."""
    state=ws.load(value);check_project(state,project)
    ws.require(state['revision']==expected,'Revision conflict: recheck the reply against current state.')
    review=plan_state(state,value,project)
    pending=[q for row in review['topics'] for q in row['pending_questions']]
    ws.require(len(pending)<=1,'Resolve multiple pending questions before replying.')
    text=reply.strip();ws.require(text,'Proposed reply is empty.')
    import stage_review
    flags=stage_review.unresolved(text,state,ws.checked_root(value),True)
    ws.require(not flags,'Reply contains unresolved evidence wording: '+json.dumps(flags,ensure_ascii=False)+'. Remove the broader claim; keep the specific supported experience. A disclaimer does not fix it.')
    narration=text.replace('’',"'")
    ws.require(not re.search(r"\b(?:check passed|here's my reply|here is my reply|sending (?:that |the )?exact reply)\b",narration,re.I),
               'Remove internal validation narration. The entire reply must be candidate-facing text only.')
    summary=text
    if pending:
        question=pending[0]['question'].strip()
        wrappers=(('**','**'),('__','__'),('*','*'),('_','_'),('"','"'),("'","'"),('“','”'),('‘','’'),('',''))
        ending=next((left+question+right for left,right in wrappers if text.endswith(left+question+right)),None)
        ws.require(ending is not None and text.count(question)==1,'End the reply with the exact saved pending question, once. Surrounding emphasis or quotes are allowed; other wording must not change.')
        summary=text[:-len(ending)]
        ws.require(not re.search(r'^\s*(?:\d+[.)]|[-*])\s+',summary,re.M),'Keep this interview reply to a short summary and the one saved question, without a checklist.')
    # WH-led declarative headings ("What I saved") are not requests without a question mark.
    direct=r'(?:^|[.!:\n]\s*)(?:please\s+)?(?:also\s+)?(?:tell me|provide|share|confirm|choose|select|let me know|send me|attach|would you|could you|can you)\b'
    indirect=r"\b(?:you (?:can|could|may|should) (?:also )?(?:share|send|provide|tell me|let me know|attach)|it (?:would|could|might|will) (?:also )?help to (?:know|have|get)|(?:please|also) (?:share|send|provide|tell me|let me know))\b"
    ws.require(not re.search(r'[?？]',summary) and not re.search(direct,summary,re.I) and not re.search(indirect,summary,re.I),
               'Reply contains an additional or unsaved request. Save one question with ask and remove the other asks before checking again.')
    return {'send_verbatim':text}



def record_statement(value, project, statement_id, text, expected):
    root=ws.checked_root(value);state=ws.load(root)
    # Recording the explicit move request must work before rebind can run.
    actual=ws.checked_root(project)
    ws.require(actual.is_dir(),'Select an existing project.')
    if Path(state.get('onboarding',{}).get('project_root',str(actual))).is_dir():
        check_project(state,actual)
    else:
        marker=actual/POINTER
        ws.require(marker.is_file() and json.loads(marker.read_text(encoding='utf-8')).get('workspace_id')==state['workspace_id'],'Moved project must retain its matching workspace pointer.')
    ws.require(state['revision']==expected,'Revision conflict: reread before recording the statement.')
    ws.require(isinstance(statement_id,str) and statement_id.strip() and text.strip(),'Stable message ID and exact statement required.')
    existing=next((r for r in state.get('statements',[]) if r['id']==statement_id),None)
    if existing:
        ws.require(existing['text']==text,'Statement ID already used for different text; use a new message ID for a correction.')
        return {'statement':existing,'revision':state['revision'],'captured_characters':len(text),'capture_instruction':CAPTURE_INSTRUCTION}
    sid='statement-'+uuid.uuid4().hex;relative='sources/'+sid+'.txt';path=ws.inside(root,relative)
    with path.open('x',encoding='utf-8') as stream:stream.write(text)
    source={'id':sid,'kind':'candidate_report','recorded_at':ws.now(),'file':relative,'sha256':ws.digest(path)}
    record={'id':statement_id,'text':text,'recorded_at':ws.now(),'source_ids':[sid]}
    state['sources'].append(source);state.setdefault('statements',[]).append(record)
    state['session']['next_action']='Map volunteered statement '+statement_id+' into supported facts and coverage; do not invent interview questions.'
    saved=ws.commit(root,state,expected,'Saved exact volunteered candidate statement')
    return {'statement':record,'revision':saved['revision'],'captured_characters':len(text),'capture_instruction':CAPTURE_INSTRUCTION}

def plan(value,project):
    return plan_state(ws.load(value),value,project)

def plan_state(state,value,project):
    check_project(state,project);ob=state['onboarding']
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
    import linkedin
    import formatting
    import provenance
    ledger=provenance.plan(state,ws.checked_root(value))
    return {'workspace_id':state['workspace_id'],'revision':state['revision'],'project_root':ob['project_root'],
        'active_track':active,'resume_status':ob['resume']['status'],'topics':rows,
        'work_history':history,
        'linkedin':linkedin.plan(state),
        'document_formats':formatting.plan(state),
        'provenance':ledger,
        'missing_baseline_topics':missing_baseline,
        'ready_to_close_interview':bool(active and has_examples and required and ob['resume']['status'] in ('read','no_resume') and not unresolved and history['ready'] and not missing_baseline and ledger['ready']),
        'unresolved_required_topics':unresolved,
        'reply_check':'Before every interview reply, including after a fact-heavy statement or when no question is saved, run check-reply on the actual proposed reply. Save one ask first if candidate input is needed; never send a list of missing topics.',
        'instruction':'Review all existing facts and exact answers for each missing dimension before asking. Map supported answers into evidence; do not repeat an answered question. Checked is derived, never an input.'}

def main():
    ws.configure_output()
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    for command in ('bind','plan','rebind','ask','save-answer','record-statement','check-reply'):
        p=sub.add_parser(command);p.add_argument('--workspace',required=True);p.add_argument('--project',required=True)
        if command in ('rebind','ask','save-answer','record-statement','check-reply'):p.add_argument('--expected-revision',type=int,required=True)
        if command=='check-reply':p.add_argument('--reply-file',required=True,help='Full proposed candidate-facing reply, not only its question')
        if command=='rebind':p.add_argument('--decision-source',required=True);p.add_argument('--workspace-id',required=True)
        if command=='ask':
            p.add_argument('--topic',required=True);p.add_argument('--dimension',required=True);p.add_argument('--question',required=True)
        if command=='record-statement':
            p.add_argument('--statement-id',required=True);p.add_argument('--text-file',required=True,help='UTF-8 text of the ENTIRE received message, including requests and postings; do not extract only personal facts')
        if command=='save-answer':
            p.add_argument('--question-id',required=True);p.add_argument('--answer-file',required=True,help='UTF-8 text containing the FULL received message, including pasted postings; not an extracted first sentence');p.add_argument('--interpretation',required=True)
    args=parser.parse_args()
    try:
        if args.command=='bind':result=bind(args.workspace,args.project)
        elif args.command=='plan':result=plan(args.workspace,args.project)
        elif args.command=='check-reply':result=check_reply(args.workspace,args.project,Path(args.reply_file).read_text(encoding='utf-8-sig'),args.expected_revision)
        elif args.command=='rebind':result=rebind(args.workspace,args.project,args.decision_source,args.expected_revision,args.workspace_id)
        elif args.command=='ask':result=ask(args.workspace,args.project,args.topic,args.dimension,args.question,args.expected_revision)
        elif args.command=='record-statement':result=record_statement(args.workspace,args.project,args.statement_id,Path(args.text_file).read_text(encoding='utf-8-sig'),args.expected_revision)
        else:result=save_answer(args.workspace,args.project,args.question_id,Path(args.answer_file).read_text(encoding='utf-8-sig'),args.interpretation,args.expected_revision)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError) as e:
        print(f'Onboarding error: {e}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
