#!/usr/bin/env python3
"""Flag stage-pack wording for evidence review; this is not a truth classifier."""
import argparse
import json
import re
import sys
import workspace as ws

PATTERNS={
 'learning_speed':r'\b(?:(?:learn\w*|pick\w*\s+up)\b[^.?!\n]{0,75}\b(?:quick\w*|fast)|(?:quick\w*|fast)\s+learn\w*)\b',
 'adaptability':r'\b(?:adaptable|adaptability)\b|\b(?:I|you|candidate)\b[^.?!\n]{0,20}\b(?:adapt(?:s|ed|ing)?\s+(?:easily|quickly|well|fast)|(?:easily|quickly|well|fast)\s+adapt(?:s|ed|ing)?)\b',
 'system_similarity':r'\b(?:similar\b[^.?!\n]{0,60}\b(?:systems?|software|platforms?|tools?|products?)|(?:systems?|software|platforms?|tools?|products?)[^.?!\n]{0,40}\bsimilar)\b',
 'role_scope':r"\b(?:(?:(?:was|were|is)(?:n\x27t| not)|not)\s+part\s+of\s+(?:[\w-]+\s+){0,4}(?:role|job)|outside\s+(?:(?:[\w-]+\s+){0,4}(?:role|job)(?:\x27s)?\s+scope|scope\s+of\s+(?:[\w-]+\s+){0,4}(?:role|job)|what\s+(?:my|the|that|this)\s+(?:role|job)\s+covered))\b"
}


def scan(text,has_submission=False):
    import calendar_review
    flags=calendar_review.scan(text)
    for number,line in enumerate(text.splitlines(),1):
        normalized=line.replace('’',"'")
        # A standalone practice question is not a candidate self-claim.
        qtext=re.sub(r'^\s*(?:[-*]\s+|\d+[.)]\s+)','',normalized).strip().strip('*_\"“” ')
        question=bool(re.match(r'^(?:how|what|why|when|where|which|who|do|does|did|can|could|would|will|are|is|have|has|tell me|describe|explain)\b',qtext,re.I)) and qtext.endswith('?') and not re.search(r'[.?!]',qtext[:-1])
        for kind,pattern in PATTERNS.items():
            employer_requirement=kind in ('system_similarity','adaptability','learning_speed') and re.match(r'^\s*Employer requirement\s*:',normalized,re.I) and not re.search(r"\b(?:I|my|candidate)\b",normalized,re.I)
            if employer_requirement:continue
            if not question and re.search(pattern,normalized,re.I):flags.append({'line':number,'kind':kind,'text':line})
        if not has_submission and re.search(r'\bsubmitted\s+(?:resume|cv|letter|materials)\b',normalized,re.I):
            flags.append({'line':number,'kind':'unverified_submission_label','text':line})
    return flags


def supported_quote(flag,state,root):
    """Resolve literal source quotations without promoting employer text to experience."""
    for quote in re.findall(r'[“\"]([^”\"\n]+)[”\"]',flag['text']):
        if flag['kind'] not in PATTERNS or not re.search(PATTERNS[flag['kind']],quote.replace('’',"'"),re.I):continue
        if re.search(PATTERNS[flag['kind']],flag['text'].replace(quote,'').replace('’',"'"),re.I):continue
        for source in state['sources']:
            candidate=source['kind'] in ('candidate_answer','candidate_report')
            employer=source['kind'] in ('employer','official') and re.match(r'^\s*(?:[-*]\s*)?Employer (?:requirement|posting|message)\s*:',flag['text'],re.I)
            if not (candidate or employer):continue
            raw=ws.inside(root,source['file']).read_text(encoding='utf-8-sig')
            if source['file'].endswith('.json'):
                data=json.loads(raw);raw=data.get('answer',data.get('text','')) if isinstance(data,dict) else ''
            if quote in raw and source['id'] in flag['text']:return True
    return False


def unresolved(text,state,root,has_submission=False):
    return [f for f in scan(text,has_submission) if f.get('severity')!='review' and not supported_quote(f,state,root)]


def guard_new_documents(old,new,root):
    known={s['id'] for s in old['sources']}
    apps={a['id']:a for a in new['applications']}
    for source in new['sources']:
        parts=source['file'].split('/')
        if source['id'] in known or source['kind']!='document' or len(parts)<3 or parts[0]!='applications' or not source['file'].lower().endswith(('.md','.txt')):continue
        app=apps.get(parts[1]);ws.require(app is not None,'Application document needs a registered application.')
        flags=unresolved(ws.inside(root,source['file']).read_text(encoding='utf-8-sig'),new,root,bool(app.get('submission')))
        ws.require(not flags,'Application document has unresolved wording: '+json.dumps(flags,ensure_ascii=False)+'. Keep only the specific sourced duty/result. For a supported flagged statement, use the exact candidate quotation with its source ID; a disclaimer does not repair a broader claim.')


def review(value,application_id,relative,fact_ids=()):
    root=ws.checked_root(value);state=ws.load(root)
    app=next((a for a in state['applications'] if a['id']==application_id),None);ws.require(app is not None,'Unknown application.')
    ws.require(relative.startswith(('scratch/','applications/'+application_id+'/')),'Review a scratch draft or this application\'s pack.')
    path=ws.inside(root,relative);ws.require(path.suffix.lower() in ('.md','.txt'),'Review plain-text Markdown or text.')
    text=path.read_text(encoding='utf-8-sig');before=ws.digest(path)
    facts={f['id']:f for f in state['profile']['facts']};ws.require(all(fid in facts for fid in fact_ids),'Unknown evidence fact ID.')
    flags=scan(text,bool(app.get('submission')))
    blocking=unresolved(text,state,root,bool(app.get('submission')))
    ws.require(ws.digest(path)==before,'Draft changed during review; scan its current version.')
    return {'file':relative,'sha256':before,'status':'review_required' if blocking or any(f.get('severity')=='review' for f in flags) else 'no_unresolved_phrase_flags','flags':flags,'unresolved_flags':blocking,
            'review_notes':[f for f in flags if f.get('severity')=='review'],
            'evidence':[{'id':fid,'claim':facts[fid]['claim'],'limits':facts[fid]['limits'],'status':facts[fid]['status'],'source_ids':facts[fid]['source_ids']} for fid in dict.fromkeys(fact_ids)],
            'limitation':'Limited English phrase scan. Questions, quoted source text and supported claims can be flagged; paraphrases can be missed. Flags are not proof of falsehood and a clear scan is not approval.',
            'next_action':'Read each flagged line against the actual candidate source. Remove unsupported self-claims; retain precise scope. Save a short resolution for justified wording. Also check promised sections, headings and the proposed chat summary. Rescan after meaningful edits, not repeatedly without changes.'}


def main():
    ws.configure_output();p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True);p.add_argument('--application',required=True);p.add_argument('--file',required=True);p.add_argument('--fact-id',action='append',default=[]);a=p.parse_args()
    try:print(json.dumps(review(a.workspace,a.application,a.file,a.fact_id),ensure_ascii=False,indent=2));return 0
    except (ws.WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:print('Stage review refused: '+str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
