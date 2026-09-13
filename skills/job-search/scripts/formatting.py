"""Sourced, occupation- and destination-scoped resume format decisions."""
import re
import workspace as ws

def active_experiences(state):
    entries=state.get('onboarding',{}).get('experiences',[])
    replaced={e['supersedes'] for e in entries if e.get('supersedes')}
    return {e['id'] for e in entries if e['id'] not in replaced}

def validate(state):
    cfg=state['integrations'].get('document_formats')
    if cfg is None:return
    ws.require(isinstance(cfg,dict) and cfg.get('version')==1,'Unknown document format configuration.')
    sources=ws.indexed(state['sources'],'sources');answers=ws.indexed(state['interviews'],'interviews')
    ob=state.get('onboarding',{});tracks=ws.indexed(ob.get('tracks',[]),'tracks')
    experiences=ws.indexed(ob.get('experiences',[]),'experiences')
    for d in ws.indexed(cfg.get('decisions'),'format decisions').values():
        ws.require(d.get('track_id') in tracks,'Document format requires a known occupation track.')
        ws.require(isinstance(d.get('country'),str) and re.fullmatch('[A-Z]{2}',d['country']),'Use a destination country code, such as CA or GB.')
        ws.require(d.get('kind') in ('resume','cv'),'Format decisions apply to resumes or CVs.')
        ws.require(d.get('page_size') in ('Letter','A4'),'Choose Letter or A4 for this destination.')
        ws.require(type(d.get('target_pages')) is int and 1<=d['target_pages']<=100,'A positive, explicit target page count is required (1-100).')
        for key in ('language','context','rationale'):
            ws.require(isinstance(d.get(key),str) and d[key].strip(),f'Format {key} is required.')
        ws.stamp(d.get('recorded_at'),'format recorded_at')
        ws.refs(d.get('source_ids'),sources,'Format authorization')
        ws.candidate_authorization(state,d,'Format authorization')
        ws.refs(d.get('convention_source_ids'),sources,'Destination guidance')
        ws.require(all(sources[s]['kind'] in ('official','employer','document','skill_reference') and sources[s].get('url') for s in d['convention_source_ids']),'Save URL-backed local/employer guidance for the destination.')
        ws.refs(d.get('experience_ids'),experiences,'Reviewed work history',False)

def guard_history(old,new):
    before=old['integrations'].get('document_formats')
    if before is None:return
    after=new['integrations'].get('document_formats')
    ws.require(after is not None and after.get('version')==before['version'],'Saved format decisions cannot be deleted.')
    ws.require(after['decisions'][:len(before['decisions'])]==before['decisions'],'Format decisions are append-only; save a new authorization.')

def scope(d):
    return (d['track_id'],d['country'],d['kind'],d['language'].casefold(),d['context'].casefold())

def plan(state):
    cfg=state['integrations'].get('document_formats')
    if not cfg:return {'status':'not_configured','decisions':[]}
    latest={scope(d):d for d in cfg['decisions']}
    active=state.get('onboarding',{}).get('active_track');history=active_experiences(state)
    return {'status':'recorded','decisions':[{**d,'history_current':set(d['experience_ids'])==history,
        'active_track':d['track_id']==active} for d in latest.values()],
        'instruction':'Use the matching destination, document kind, language and context. Review material history changes before changing or reusing the approved length.'}

def for_model(model,state):
    if model['kind']=='cover_letter':return None
    did=model.get('format_decision_id')
    choices=plan(state)['decisions']
    if not choices and did is None:return None  # Older files remain drafts, not approved formats.
    d=next((d for d in choices if d['id']==did),None)
    ws.require(d is not None,'Select the latest saved format decision for this resume/CV scope.')
    ws.require(d['active_track'],'Format decision belongs to another occupation.')
    ws.require(d['history_current'],'Work history changed: review the length recommendation and save a new authorization.')
    for field,model_field in (('country','target_country'),('kind','kind'),('language','language'),('context','document_context'),('page_size','page_size')):
        ws.require(model.get(model_field)==d[field],f'Document {model_field} does not match the approved destination format.')
    sources=ws.indexed(state['sources'],'sources')
    d['guidance_status']='provisional_skill_reference' if any(sources[x]['kind']=='skill_reference' for x in d['convention_source_ids']) else 'recorded_external_source'
    return d
