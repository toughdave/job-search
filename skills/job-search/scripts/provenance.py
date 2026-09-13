#!/usr/bin/env python3
"""Save a versioned provenance ledger and its current pointer in one state commit."""
import argparse
import hashlib
import json
import re
import sys
import workspace as ws

PATTERN=re.compile(r'^notes/provenance-ledger-v(\d+)\.md$')
STATUSES={'confirmed','corrected','denied_by_candidate','unverified','conflict_pending','excluded_on_current_evidence'}


def review_text(body,state=None,root=None):
    prose=re.sub(r'^```json\s*\n.*?^```\s*$','',body,flags=re.M|re.S)
    for number,line in enumerate(prose.splitlines(),1):
        ws.require(not re.search(r'\b(?:excluded? permanently|permanently exclud\w*|permanent (?:ban|exclusion))\b',line,re.I),f'Ledger line {number}: exclusion depends on current evidence, not a permanent ban. Preserve the old version by link and write the current resolution.')
        ws.require(not (re.search(r'\b(?:false|disproven|denied)\b',line,re.I) and re.search(r'\b(?:unconfirmed|unverified|unmeasured|unknown)\b',line,re.I)),f'Ledger line {number}: separate conflicting resolution statuses into individual claim rows. An unmeasured result is unverified; a denied tool or duty is a separate claim.')
    blocks=re.findall(r'^```json\s*\n(.*?)^```\s*$',body,re.M|re.S)
    ws.require(len(blocks)==1,'New ledgers require one JSON block containing a claims list; see references/provenance.md. Historical ledgers remain readable.')
    data=json.loads(blocks[0]);claims=data.get('claims') if isinstance(data,dict) else None
    ws.require(isinstance(claims,list) and claims,'Ledger claims must be a nonempty list.')
    rows=ws.indexed(claims,'provenance claims')
    sources={s['id']:s for s in state['sources']} if state is not None else {}
    for row in rows.values():
        ws.require(row.get('status') in STATUSES,'Use one fixed provenance status per claim: '+', '.join(sorted(STATUSES)))
        ws.require(isinstance(row.get('claim'),str) and row['claim'].strip(),'Claim must contain the exact original excerpt as a JSON string.')
        ws.require(isinstance(row.get('source_id'),str) and row['source_id'],'Claim source_id required.')
        ws.require(isinstance(row.get('rationale'),str) and row['rationale'].strip(),'Claim rationale required; it is advisory, not another status.')
        if state is not None:
            ws.require(row['source_id'] in sources,'Unknown original claim source.')
            source=sources[row['source_id']];path=ws.inside(root,source['file'])
            ws.require(path.suffix.lower() in ('.txt','.md','.json'),'Link readable saved source text for the original excerpt.')
            raw=path.read_text(encoding='utf-8-sig')
            if path.suffix.lower()=='.json':
                payload=json.loads(raw);raw=payload.get('answer',payload.get('text','')) if isinstance(payload,dict) else ''
            ws.require(row['claim'] in raw,'Claim must be an exact excerpt from its linked source; do not generalize its scope.')
            resolution=row.get('resolution_source_ids',[]);ws.refs(resolution,sources,'Claim resolution',False)
            if row['status'] in ('corrected','denied_by_candidate'):
                ws.require(any(sources[s]['kind'] in ('candidate_answer','candidate_report') for s in resolution),'A correction or denial needs a candidate answer/report source.')
    return claims


def guard_new_documents(old,new,root):
    known={s['id'] for s in old['sources']}
    for _,source in registered(new):
        if source['id'] not in known:review_text(ws.inside(root,source['file']).read_text(encoding='utf-8-sig'),new,root)


def registered(state):
    rows=[]
    for source in state['sources']:
        match=PATTERN.fullmatch(source['file'])
        if match and source['kind']=='document':rows.append((int(match[1]),source))
    ws.require(len({n for n,s in rows})==len(rows),'Conflicting ledger version registrations; inspect sources before updating.')
    return sorted(rows,key=lambda row:row[0])


def reference(source):return {k:source[k] for k in ('file','sha256')}|{'source_id':source['id']}


def validate(state,root):
    registered(state)
    pointer=state.get('onboarding',{}).get('resume',{}).get('provenance_ledger')
    if pointer is None:return
    ws.require(isinstance(pointer,dict),'Provenance pointer must be an object.')
    sources={s['id']:s for s in state['sources']};source=sources.get(pointer.get('source_id'))
    ws.require(source and source['kind']=='document' and reference(source)==pointer,'Provenance pointer must match its registered document source, file and hash.')
    ws.file_ref(root,pointer,'Provenance ledger')


def guard_history(old,new):
    old_rows=registered(old);new_rows=registered(new)
    old_latest=reference(old_rows[-1][1]) if old_rows else None
    latest=reference(new_rows[-1][1]) if new_rows else None
    old_pointer=old.get('onboarding',{}).get('resume',{}).get('provenance_ledger')
    pointer=new.get('onboarding',{}).get('resume',{}).get('provenance_ledger')
    if latest!=old_latest or pointer!=old_pointer:
        ws.require(pointer==latest,'Register the latest ledger and its current pointer together; use provenance.py save or repair.')


def plan(state,root):
    intake=state.get('onboarding',{}).get('resume',{})
    sources={s['id']:s for s in state['sources']}
    resume_ids=[sid for sid in intake.get('source_ids',[]) if sources.get(sid,{}).get('kind')=='resume']
    rows=registered(state);latest=reference(rows[-1][1]) if rows else None
    pointer=intake.get('provenance_ledger');known={s['file'] for s in state['sources']}
    pending=[p.relative_to(root).as_posix() for p in ws.inside(root,'notes').glob('provenance-ledger-v*.md') if p.relative_to(root).as_posix() not in known]
    required=len(resume_ids)>=2 or bool(rows or pointer or pending)
    ready=not required or bool(latest and pointer==latest and not pending)
    return {'required':required,'ready':ready,'current':pointer,'latest_registered':latest,'unregistered_files':sorted(pending),
            'next_action':None if ready else 'Save the current ledger with provenance.py save, or repair a stale pointer with repair. Inspect unregistered files before resuming an interrupted save.'}


def save(value,draft,expected):
    root=ws.checked_root(value);state=ws.load(root)
    ws.require(state['revision']==expected,'Revision conflict: reread before saving the ledger.')
    ws.require('onboarding' in state,'Bind the project interview before saving its ledger.')
    path=ws.inside(root,draft);ws.require(draft.startswith('scratch/'),'Prepare the ledger draft in workspace scratch.')
    body=path.read_text(encoding='utf-8-sig').strip();ws.require(body,'Ledger draft is empty.')
    review_text(body,state,root)
    digest=hashlib.sha256(body.encode('utf-8')).hexdigest();rows=registered(state)
    latest=rows[-1][1] if rows else None;intake=state['onboarding']['resume']
    if latest and latest.get('draft_sha256')==digest and latest.get('resume_source_ids')==intake.get('source_ids',[]):
        if intake.get('provenance_ledger')==reference(latest):return {'ledger':reference(latest),'revision':state['revision']}
        return repair(root,expected)
    version=rows[-1][0]+1 if rows else 1
    sid=f'provenance-ledger-v{version:03d}';relative=f'notes/{sid}.md'
    ws.require(not any(s['id']==sid for s in state['sources']),'Ledger source ID already used; inspect the existing source.')
    previous=f"Previous ledger: [{latest['id']}]({latest['file'].split('/')[-1]})\n\n" if latest else ''
    prepared=ws.inside(root,'scratch/provenance-prepared-'+digest+'.md');prepared.write_text(previous+body+'\n',encoding='utf-8')
    ref=ws.import_file(root,prepared,relative)
    source={'id':sid,'kind':'document','recorded_at':ws.now(),**ref,'draft_sha256':digest,'resume_source_ids':list(intake.get('source_ids',[]))}
    if latest:source['previous_source_id']=latest['id']
    state['sources'].append(source);intake['provenance_ledger']=reference(source)
    saved=ws.commit(root,state,expected,'Saved provenance ledger and current pointer together')
    return {'ledger':saved['onboarding']['resume']['provenance_ledger'],'revision':saved['revision']}


def repair(value,expected):
    root=ws.checked_root(value);state=ws.load(root)
    ws.require(state['revision']==expected,'Revision conflict: reread before repairing the pointer.')
    ws.require('onboarding' in state,'Bind the project first.')
    rows=registered(state);ws.require(rows,'No registered ledger to point to; save the draft first.')
    pointer=reference(rows[-1][1]);intake=state['onboarding']['resume']
    if intake.get('provenance_ledger')!=pointer:
        intake['provenance_ledger']=pointer;state=ws.commit(root,state,expected,'Reconciled current provenance pointer to latest registered ledger')
    return {'ledger':pointer,'revision':state['revision']}


def main():
    ws.configure_output();p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('plan','save','repair'));p.add_argument('--workspace',required=True);p.add_argument('--draft');p.add_argument('--expected-revision',type=int)
    a=p.parse_args()
    try:
        if a.command=='plan':root=ws.checked_root(a.workspace);result=plan(ws.load(root),root)
        else:
            ws.require(a.expected_revision is not None,'Expected revision required.')
            if a.command=='save':ws.require(a.draft,'A draft path is required.');result=save(a.workspace,a.draft,a.expected_revision)
            else:result=repair(a.workspace,a.expected_revision)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ws.WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:print('Provenance operation refused: '+str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
