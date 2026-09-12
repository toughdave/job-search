#!/usr/bin/env python3
"""Guarded private workspace storage. Python 3.10+, standard library only."""
import argparse
import copy
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

SCHEMA = 1
STAGES = {'discovered','qualified','preparing','ready','submitted_unverified','submitted','blocked','skipped','withdrawn'}
OUTCOMES = {'none','awaiting','positive','action','offer','declined'}
POSTINGS = {'unknown','open','closed','expired','cancelled'}
KINDS = {'resume','candidate_answer','document','employer','official','candidate_report'}
FACT_STATUS = {'candidate_reported','verified','unresolved','superseded'}
CATEGORIES = {'employment','project','volunteering','education','certification','skill','preference','identity','other'}
BUCKETS = {'sources','applications','documents','notes'}

class WorkspaceError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise WorkspaceError(message)

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def checked_root(value):
    root = Path(value).absolute()
    require(root.parent != root, 'A drive/filesystem root cannot be a workspace.')
    for part in [root, *root.parents]:
        require(not part.is_symlink() and not (hasattr(part,'is_junction') and part.is_junction()),
                'Workspace paths may not contain symlinks or junctions.')
    require(root.resolve() == root, 'Workspace must use a direct absolute path.')
    return root

def inside(root, relative):
    require(isinstance(relative,str) and relative, 'A relative file path is required.')
    require('\\' not in relative and ':' not in relative, 'Use relative forward-slash paths without drive names.')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and all(p not in ('..','.') for p in path.parts), 'Path escapes the workspace.')
    require(not any(p.endswith((' ','.')) or re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?',p,re.I) for p in path.parts), 'Unsafe cross-platform filename.')
    dest = root.joinpath(*path.parts)
    require(dest.resolve().is_relative_to(root), 'Path escapes the workspace.')
    for part in [dest, *dest.parents]:
        if part == root.parent:
            break
        require(not part.is_symlink() and not (hasattr(part,'is_junction') and part.is_junction()), 'Symlinks and junctions are not allowed.')
    return dest

def atomic_json(path, value):
    data = (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    fd, tmp = tempfile.mkstemp(prefix='.write-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def stamp(value, label):
    require(isinstance(value,str), f'{label}: timestamp required.')
    try:
        dt = datetime.fromisoformat(value.replace('Z','+00:00'))
        require(dt.tzinfo is not None, f'{label}: include timezone.')
    except (ValueError,TypeError):
        raise WorkspaceError(f'{label}: valid timestamp with timezone required.')

def canonical(url):
    require(isinstance(url,str), 'URL must be text.')
    if not url: return ''
    p = urlsplit(url)
    require(p.scheme.lower() in ('http','https') and p.hostname and not p.username and not p.password, 'Only public HTTP(S) URL shapes without credentials are allowed.')
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted((k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith('utm_') and k.lower() not in ('source','ref','trackingid'))),''))

def indexed(items, label):
    require(isinstance(items,list), f'{label} must be a list.')
    result = {}
    for item in items:
        require(isinstance(item,dict), f'{label} entries must be objects.')
        key = item.get('id')
        require(isinstance(key,str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}',key), f'{label}: invalid id.')
        require(key not in result, f'{label}: duplicate id {key}.')
        result[key] = item
    return result

def refs(ids, source_map, label, nonempty=True):
    require(isinstance(ids,list) and (ids or not nonempty), f'{label}: source IDs required.')
    require(all(isinstance(x,str) and x in source_map for x in ids), f'{label}: unknown source reference.')

def file_ref(root, item, label):
    require(isinstance(item,dict), f'{label}: file reference required.')
    p = inside(root,item.get('file'))
    require(PurePosixPath(item['file']).as_posix().casefold() != 'notes/status.md', f'{label}: derived STATUS.md cannot be evidence.')
    require(PurePosixPath(item['file']).parts[0] in BUCKETS, f'{label}: file is not in a content folder.')
    require(p.is_file(), f'{label}: file is missing.')
    require(item.get('sha256') == digest(p), f'{label}: saved file hash differs.')

def validate(state, root):
    require(isinstance(state,dict) and state.get('schema_version')==SCHEMA, 'Unsupported workspace schema; preserve it and use a compatible release.')
    require(isinstance(state.get('revision'),int) and state['revision']>=0, 'Invalid revision.')
    require(isinstance(state.get('workspace_id'),str) and state['workspace_id'], 'Workspace identity missing.')
    stamp(state.get('created_at'),'created_at'); stamp(state.get('updated_at'),'updated_at')
    profile=state.get('profile'); require(isinstance(profile,dict),'Profile must be an object.')
    sources=indexed(state.get('sources'),'sources')
    for s in sources.values():
        require(s.get('kind') in KINDS, 'Invalid evidence source kind.')
        stamp(s.get('recorded_at'),'source recorded_at'); file_ref(root,s,'Source')
        if s.get('url'): canonical(s['url'])
    interviews=indexed(state.get('interviews'),'interviews')
    for q in interviews.values():
        require(all(isinstance(q.get(k),str) and q[k].strip() for k in ('question','answer','interpretation')), 'Interview needs exact question, answer and interpretation.')
        refs(q.get('source_ids'),sources,'Interview'); stamp(q.get('recorded_at'),'interview recorded_at')
    facts=indexed(profile.get('facts'),'facts')
    for f in facts.values():
        require(isinstance(f.get('claim'),str) and f['claim'].strip(),'Fact needs a claim.')
        require(f.get('status') in FACT_STATUS and f.get('category') in CATEGORIES,'Invalid fact category/status.')
        require(isinstance(f.get('limits'),str),'Fact scope limits must be text, possibly empty.')
        refs(f.get('source_ids'),sources,'Fact',nonempty=f['status']!='unresolved')
        if f['status']=='verified':
            require(any(sources[x]['kind'] in ('document','official','employer') for x in f['source_ids']), 'Verified fact requires independent evidence.')
        for old in f.get('supersedes',[]):
            require(old in facts and facts[old]['status']=='superseded' and old!=f['id'],'Correction must reference a superseded fact.')
    prefs=profile.get('preferences'); require(isinstance(prefs,dict),'Preferences must be an object.')
    for p in prefs.values():
        require(isinstance(p,dict) and 'value' in p,'Preference needs a value.'); refs(p.get('source_ids'),sources,'Preference')
    decisions=indexed(state.get('decisions'),'decisions')
    for d in decisions.values():
        require(isinstance(d.get('decision'),str) and isinstance(d.get('scope'),str),'Decision and scope required.')
        refs(d.get('source_ids'),sources,'Decision')
    apps=indexed(state.get('applications'),'applications'); seen=set()
    for a in apps.values():
        require(all(isinstance(a.get(k),str) for k in ('employer','role','job_id','url','location','next_action')),'Application text fields missing.')
        require(a['employer'].strip() and a['role'].strip(),'Employer and role required.')
        require(a.get('stage') in STAGES and a.get('outcome') in OUTCOMES and a.get('posting_status') in POSTINGS,'Invalid application state.')
        url=canonical(a['url']); emp=a['employer'].strip().casefold(); job=a['job_id'].strip().casefold()
        key=(emp,'id',job) if job else ((emp,'url',url) if url else None)
        require(key is None or key not in seen,'Duplicate employer/requisition or canonical URL.')
        if key: seen.add(key)
        refs(a.get('source_ids',[]),sources,'Application sources',False)
        if a['posting_status']!='unknown': refs(a.get('posting_source_ids'),sources,'Posting status')
        refs(a.get('outcome_source_ids',[]),sources,'Outcome evidence',False)
        if a['outcome'] in ('positive','action','offer','declined'):
            require(any(sources[x]['kind']=='employer' for x in a.get('outcome_source_ids',[])),'Employer outcome requires an employer source.')
        if a['outcome']=='awaiting': require(a['stage'] in ('submitted','submitted_unverified','withdrawn'),'Awaiting requires a submission stage.')
        submission=a.get('submission')
        if a['stage']=='submitted':
            require(isinstance(submission,dict) and submission,'Confirmed submission evidence required.')
        if submission is not None:
            require(isinstance(submission,dict) and submission,'Submission receipt must be a nonempty object.')
            stamp(submission.get('confirmed_at'),'confirmed_at'); refs(submission.get('source_ids'),sources,'Submission')
            require(any(sources[x]['kind']=='employer' for x in submission['source_ids']),'Submission needs employer confirmation.')
            require(isinstance(submission.get('files'),list) and submission['files'],'Submitted file snapshot required.')
            for f in submission['files']: file_ref(root,f,'Submitted file')
        if a['stage']=='submitted_unverified': require(not submission,'Unverified submission cannot have a confirmed receipt/date.')
        for m in a.get('fit',[]):
            require(isinstance(m,dict) and isinstance(m.get('requirement'),str),'Fit requirement required.')
            require(m.get('assessment') in ('supported','unknown','gap','not_required'),'Fit assessment invalid.')
            ids=m.get('fact_ids',[]); require(isinstance(ids,list) and all(x in facts for x in ids),'Unknown fit fact.')
            if m['assessment']=='supported': require(ids and all(facts[x]['status'] in ('verified','candidate_reported') for x in ids),'Supported fit cannot use unresolved/superseded facts.')
    runs=indexed(state.get('runs'),'runs')
    for r in runs.values():
        require(r.get('status') in ('running','complete','incomplete'),'Invalid run status.')
        require(isinstance(r.get('scope'),str) and r['scope'].strip(),'Run scope required.')
        checks=r.get('checks'); require(isinstance(checks,list),'Run checks required.')
        for c in checks:
            require(c.get('status') in ('complete','partial','blocked','not_configured'),'Invalid source coverage.')
            require(isinstance(c.get('required'),bool) and isinstance(c.get('source'),str) and isinstance(c.get('query'),str),'Coverage source, query and required flag needed.')
            stamp(c.get('checked_at'),'coverage checked_at')
            require(isinstance(c.get('inspected'),int) and c['inspected']>=0,'Inspected count required.')
            refs(c.get('source_ids',[]),sources,'Coverage evidence',nonempty=c['status']=='complete')
        if r['status']=='complete':
            require(checks and all(c['status']=='complete' for c in checks if c['required']),'Incomplete required coverage cannot certify a complete run.')
            require(any(c['required'] for c in checks),'Complete run needs a required check.')
    for p in indexed(state.get('pending_actions'),'pending_actions').values():
        require(p.get('application_id') in apps and p.get('status') in ('pending','resolved'),'Invalid pending action.')
        require(isinstance(p.get('action'),str) and isinstance(p.get('next_check'),str),'Pending action needs action and recovery check.')
    require(isinstance(state.get('session'),dict) and isinstance(state['session'].get('next_action'),str),'Next action required.')
    require(isinstance(state.get('integrations'),dict),'Integrations must be an object.')
    require(isinstance(state.get('history'),list),'History required.')
    return state

def load(root):
    root=checked_root(root)
    marker=inside(root,'.job-search-workspace.json'); path=inside(root,'.job-search/state.json')
    require(marker.is_file() and path.is_file(),'Not an initialized Job Search Starter Kit workspace. Refusing to adopt existing files.')
    meta=json.loads(marker.read_text(encoding='utf-8'))
    state=json.loads(path.read_text(encoding='utf-8'))
    require(meta.get('format')=='job-search-starter-kit' and meta.get('workspace_id')==state.get('workspace_id'),'Workspace identity mismatch.')
    return validate(state,root)

def initialize(value):
    root=checked_root(value)
    require(not root.exists(),'Initialize requires a NEW directory; existing folders are never adopted or overwritten.')
    require(root.parent.is_dir(),'Choose an existing writable parent folder.')
    for parent in root.parents:
        require(not (parent/'SKILL.md').exists() and not (parent/'.git').exists(),'Private workspace must be outside an installed skill and source repository.')
    root.mkdir()
    (root/'.job-search').mkdir(); (root/'.job-search/backups').mkdir()
    for bucket in BUCKETS: (root/bucket).mkdir()
    ts=now(); wid=str(uuid.uuid4())
    state={'schema_version':SCHEMA,'workspace_id':wid,'revision':0,'created_at':ts,'updated_at':ts,'profile':{'facts':[],'preferences':{}},'sources':[],'interviews':[],'decisions':[],'applications':[],'runs':[],'pending_actions':[],'integrations':{},'session':{'next_action':'Read the supplied resume and ask the next useful question.'},'history':[]}
    atomic_json(root/'.job-search-workspace.json',{'format':'job-search-starter-kit','workspace_id':wid})
    atomic_json(root/'.job-search/state.json',state)
    (root/'.gitignore').write_text('*\n',encoding='utf-8')
    status_note(root,state)
    return state

def status_note(root,state):
    # Derived view only. Failure cannot invalidate a committed authoritative state.
    p=inside(root,'notes/STATUS.md')
    txt=f"# Your job search\n\nSaved revision: {state['revision']}\n\nNext action: {state['session']['next_action']}\n\nApplications tracked: {len(state['applications'])}\n\nThe AI maintains these files for you. Continue in the same project or supply this workspace location.\n"
    p.write_text(txt,encoding='utf-8')

def guard_history(old,new):
    for name in ('sources','interviews','decisions'):
        before=indexed(old[name],name); after=indexed(new[name],name)
        require(all(k in after and after[k]==v for k,v in before.items()),f'{name} is append-only; add a correction instead of overwriting history.')
    before=indexed(old['profile']['facts'],'facts'); after=indexed(new['profile']['facts'],'facts')
    for k,v in before.items():
        require(k in after,'Facts cannot be deleted; supersede them.')
        changed=copy.deepcopy(v); changed['status']='superseded'
        require(after[k]==v or after[k]==changed,'Correct a fact by superseding it and adding a new fact, not rewriting it.')
    oldapps=indexed(old['applications'],'applications'); newapps=indexed(new['applications'],'applications')
    for k,v in oldapps.items():
        require(k in newapps,'Application history cannot be deleted.')
        if v.get('submission'):
            require(newapps[k].get('submission')==v['submission'],'Confirmed submission snapshots are immutable.')
    require(new['history']==old['history'],'The helper owns the commit history.')

@contextmanager
def write_lock(value):
    root=checked_root(value); load(root)
    lock=inside(root,'.job-search/write.lock'); token=str(uuid.uuid4())
    try:
        fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    except FileExistsError:
        raise WorkspaceError('Another writer or an interrupted write owns the lock. Inspect its owner; never steal it based on age.')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump({'token':token,'pid':os.getpid(),'started_at':now()},f)
        yield root
    finally:
        if lock.exists():
            try:
                if json.loads(lock.read_text()).get('token')==token: lock.unlink()
            except (OSError,ValueError): pass


def commit(value,candidate,expected,summary):
    with write_lock(value) as root:
        old=load(root)
        require(old['revision']==expected,'Revision conflict: reread current state and merge your intended change.')
        new=copy.deepcopy(candidate)
        require(new.get('workspace_id')==old['workspace_id'] and new.get('created_at')==old['created_at'],'Cannot change workspace identity.')
        require(new.get('revision')==expected,'Draft revision must match the state you read.')
        validate(new,root); guard_history(old,new)
        new['revision']=expected+1; new['updated_at']=now()
        new['history'].append({'revision':new['revision'],'at':new['updated_at'],'summary':summary})
        backup=inside(root,f".job-search/backups/state-{expected:06d}-{uuid.uuid4().hex[:8]}.json")
        atomic_json(backup,old); atomic_json(inside(root,'.job-search/state.json'),new)
        try: status_note(root,new)
        except OSError: pass
        return load(root)

def import_file(value,source,relative):
    root=checked_root(value); load(root)
    require(isinstance(relative,str) and relative,'A relative file path is required.')
    require(PurePosixPath(relative).as_posix().casefold() != 'notes/status.md','Derived STATUS.md is reserved; choose another filename.')
    require(PurePosixPath(relative).parts[0] in BUCKETS,'Files must be in sources, applications, documents or notes.')
    dest=inside(root,relative); src=Path(source)
    require(src.is_file(),'Source file is missing.')
    require(src.stat().st_size<=25*1024*1024,'File exceeds the 25 MiB per-file limit.')
    data=src.read_bytes(); dest.parent.mkdir(parents=True,exist_ok=True)
    # Recheck after creating directories, then publish without replacing an existing file.
    dest=inside(root,relative)
    if dest.exists():
        require(dest.is_file() and dest.read_bytes()==data,'Existing content is immutable; choose a new version filename.')
    else:
        with dest.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    return {'file':relative,'sha256':digest(dest)}

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    for command in ('init','show','validate','commit','import-file'):
        q=sub.add_parser(command); q.add_argument('--workspace',required=True)
        if command=='commit':
            q.add_argument('--input',required=True); q.add_argument('--expected-revision',type=int,required=True); q.add_argument('--summary',required=True)
        if command=='import-file': q.add_argument('--source',required=True); q.add_argument('--relative',required=True)
    args=p.parse_args()
    try:
        if args.command=='init': result=initialize(args.workspace)
        elif args.command=='commit': result=commit(args.workspace,json.loads(Path(args.input).read_text(encoding='utf-8')),args.expected_revision,args.summary)
        elif args.command=='import-file': result=import_file(args.workspace,args.source,args.relative)
        else: result=load(args.workspace)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:
        print(f'Workspace error: {e}',file=sys.stderr); return 2
    return 0

if __name__=='__main__': sys.exit(main())
