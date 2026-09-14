"""Project-local mail consent and account checks; does not connect or read mail."""
import argparse,json,re,sys,uuid
from datetime import datetime,timezone
import workspace as ws

EMAIL=r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,}'

def email(value):
    ws.require(isinstance(value,str) and re.fullmatch(EMAIL,value.strip()),'A complete email address is required.')
    return value.strip().casefold()  # Never silently strip dots, tags or change domains.

def fact_email(state,fid):
    fact=next((f for f in state['profile']['facts'] if f['id']==fid),None)
    ws.require(fact is not None,'Unknown application-email fact.')
    found=re.findall(EMAIL,fact['claim'])
    ws.require(len(found)==1,'Application-email fact must contain exactly one address.')
    return email(found[0]),fact['status'] in ('candidate_reported','verified')

def validate(state,root):
    cfg=state['integrations'].get('mail')
    if cfg is None:return
    ws.require(isinstance(cfg,dict) and cfg.get('version')==1,'Unknown mail setup format.')
    ws.require(cfg.get('choice') in ('enabled','declined','deferred'),'Invalid mail choice.')
    sources=ws.indexed(state['sources'],'sources')
    ws.refs(cfg.get('decision_source_ids'),sources,'Mail permission')
    ws.require(all(sources[x]['kind'] in ('candidate_answer','candidate_report') for x in cfg['decision_source_ids']),'Mail choice needs the candidate response.')
    ws.require(cfg.get('scope')=='job_search_read','This mail setup grants job-search reads only.')
    if cfg['choice']=='enabled':
        fact_email(state,cfg.get('email_fact_id'));email(cfg.get('application_email'));email(cfg.get('mailbox_email'))
        ws.require(type(cfg.get('lookback_days')) is int and 1<=cfg['lookback_days']<=365,'Use a bounded mail lookback of 1 to 365 days.')
    for binding in cfg.get('bindings',[]):
        ws.require(binding.get('harness') in ('codex','claude-code','other'),'Unknown mail harness.')
        ws.require(isinstance(binding.get('connector'),str) and binding['connector'].strip(),'Connector identity required.')
        email(binding.get('authenticated_email'));ws.stamp(binding.get('checked_at'),'mail verification')
        ws.refs([binding.get('source_id')],sources,'Mail verification')
        source=sources[binding['source_id']]
        ws.require(source['kind']=='official','Mail verification must be connector evidence, not a candidate assertion.')
        data=json.loads(ws.inside(root,source['file']).read_text(encoding='utf-8'))
        ws.require(data==binding['observation'],'Saved mail observation differs from the verified source.')
        validate_observation(data)
        ws.require(all(binding[k]==data[k] for k in ('harness','connector','authenticated_email','checked_at')),'Mail binding/source mismatch.')

def validate_observation(data):
    allowed={'harness','connector','authenticated_email','checked_at','identity_tool','identity_call_id','read_tool','read_call_id','read_status','query','inspected'}
    ws.require(isinstance(data,dict) and set(data)==allowed,'Use only the documented sanitized mail observation fields; never tokens or message bodies.')
    ws.require(data['harness'] in ('codex','claude-code','other'),'Unknown harness.')
    for key in ('connector','identity_tool','identity_call_id'):
        ws.require(isinstance(data[key],str) and data[key].strip(),'Identity tool evidence required.')
    email(data['authenticated_email']);ws.stamp(data['checked_at'],'mail checked_at')
    ws.require(data['read_status'] in ('complete','blocked','not_attempted'),'Invalid mail read result.')
    ws.require(type(data['inspected']) is int and 0<=data['inspected']<=20,'Keep setup read bounded to 20 results.')
    for key in ('read_tool','read_call_id','query'):ws.require(isinstance(data[key],str),'Mail read metadata must be text.')
    if data['read_status']=='complete':ws.require(all(data[k].strip() for k in ('read_tool','read_call_id','query')),'Successful read needs actual tool and query evidence, even for zero results.')

def choose(root,choice,decision_ids,expected,email_fact_id=None,mailbox_email=None,lookback_days=14):
    root=ws.checked_root(root);state=ws.load(root)
    ws.require(state['revision']==expected,'Revision conflict: reread mail setup.')
    cfg={'version':1,'choice':choice,'decision_source_ids':decision_ids,'scope':'job_search_read','bindings':[]}
    if choice=='enabled':
        address,current=fact_email(state,email_fact_id);ws.require(current,'Confirm a current application-email fact first.')
        cfg.update(email_fact_id=email_fact_id,application_email=address,mailbox_email=email(mailbox_email or address),lookback_days=lookback_days)
    state['integrations']['mail']=cfg
    return ws.commit(root,state,expected,'Saved candidate mail choice; prior account checks must be repeated')

def observe(root,relative,expected):
    root=ws.checked_root(root);state=ws.load(root)
    ws.require(state['revision']==expected,'Revision conflict: reread mail setup.')
    cfg=state['integrations'].get('mail');ws.require(cfg and cfg['choice']=='enabled','No current permission for mailbox verification.')
    data=json.loads(ws.inside(root,relative).read_text(encoding='utf-8-sig'));validate_observation(data)
    data['authenticated_email']=email(data['authenticated_email'])
    ws.require(data['read_status']!='complete' or data['authenticated_email']==cfg['mailbox_email'],'Do not test inbox contents in a mismatched account. Reconnect the selected mailbox first.')
    sid='mail-'+uuid.uuid4().hex;path=ws.inside(root,'sources/'+sid+'.json');ws.atomic_json(path,data)
    state['sources'].append({'id':sid,'kind':'official','file':'sources/'+sid+'.json','sha256':ws.digest(path),'recorded_at':ws.now()})
    cfg['bindings'].append({k:data[k] for k in ('harness','connector','authenticated_email','checked_at')})
    cfg['bindings'][-1].update(source_id=sid,observation=data)
    return ws.commit(root,state,expected,'Saved host-specific mail identity and bounded-read observation')

def plan(state,harness=None,authenticated_email=None,now=None):
    cfg=state['integrations'].get('mail')
    def result(status,**kw):return {'status':status,'ready_for_read':status=='ready',**kw}
    if cfg is None:return result('not_configured')
    if cfg['choice']!='enabled':return result(cfg['choice'])
    address,current=fact_email(state,cfg['email_fact_id'])
    if not current or address!=cfg['application_email']:return result('email_changed')
    chosen=cfg['mailbox_email']
    if harness is None:return result('select_harness',mailbox_email=chosen)
    records=[x for x in cfg['bindings'] if x['harness']==harness]
    if not records:return result('needs_connection',mailbox_email=chosen,harness=harness)
    binding=records[-1];detail={'mailbox_email':chosen,'harness':harness,'connector':binding['connector'],'lookback_days':cfg['lookback_days']}
    if binding['authenticated_email']!=chosen:return result('account_mismatch',**detail)
    stamp=datetime.fromisoformat(binding['checked_at']);instant=now or datetime.now(timezone.utc)
    if not 0<=(instant-stamp).total_seconds()<=86400:return result('verification_stale',**detail)
    if binding['observation']['read_status']!='complete':return result('read_unavailable',**detail)
    if authenticated_email is None:return result('needs_live_identity_check',**detail)
    if email(authenticated_email)!=chosen:return result('account_mismatch',**detail)
    return result('ready',**detail)

def guard_run_completion(old,new):
    # Historical completed runs remain readable after permission/account changes.
    if 'mail' not in new['integrations']:return
    before={r['id']:r for r in old['runs']}
    for run in new['runs']:
        if run.get('status')!='complete' or before.get(run['id'],{}).get('status')=='complete' or 'mail' not in run.get('required_checks',[]):continue
        valid=False
        for binding in new['integrations']['mail'].get('bindings',[]):
            if not plan(new,binding['harness'],binding['authenticated_email'])['ready_for_read']:continue
            if datetime.fromisoformat(binding['checked_at'])<datetime.fromisoformat(run['started_at']):continue
            if any(c.get('source')=='mail' and c.get('status')=='complete' and binding['source_id'] in c.get('source_ids',[]) for c in run['checks']):valid=True
        ws.require(valid,'Required mail coverage needs this run\'s matched-account read evidence; keep the run incomplete when mail is unavailable.')


def main():
    ws.configure_output();p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    for command in ('choose','observe','plan'):
        a=sub.add_parser(command);a.add_argument('--workspace',required=True)
        if command!='plan':a.add_argument('--expected-revision',required=True,type=int)
        if command=='choose':
            a.add_argument('--choice',required=True,choices=('enabled','declined','deferred'));a.add_argument('--decision-source',required=True,action='append');a.add_argument('--email-fact');a.add_argument('--mailbox-email');a.add_argument('--lookback-days',type=int,default=14)
        if command=='observe':a.add_argument('--file',required=True)
        if command=='plan':a.add_argument('--harness',choices=('codex','claude-code','other'));a.add_argument('--authenticated-email')
    a=p.parse_args()
    try:
        if a.command=='choose':state=choose(a.workspace,a.choice,a.decision_source,a.expected_revision,a.email_fact,a.mailbox_email,a.lookback_days);output={'revision':state['revision'],'mail':plan(state)}
        elif a.command=='observe':state=observe(a.workspace,a.file,a.expected_revision);output={'revision':state['revision'],'mail':plan(state)}
        else:output=plan(ws.load(a.workspace),a.harness,a.authenticated_email)
        print(json.dumps(output,indent=2));return 0
    except (ws.WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:print('Mail setup refused: '+str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
