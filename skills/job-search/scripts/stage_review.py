#!/usr/bin/env python3
"""Flag stage-pack wording for evidence review; this is not a truth classifier."""
import argparse
import json
import re
import sys
import workspace as ws

PATTERNS={
 'learning_speed':r'\b(?:(?:learn\w*|pick\w*\s+up)\b[^.?!\n]{0,75}\b(?:quick\w*|fast)|(?:quick\w*|fast)\s+learn\w*)\b',
 'adaptability':r'\badapt(?:able|ability|s|ed|ing)?\b',
 'system_similarity':r'\bsimilar\b',
 'role_scope':r"\b(?:(?:(?:was|were|is)(?:n\x27t| not)|not)\s+part\s+of\s+(?:[\w-]+\s+){0,4}(?:role|job)|outside\s+(?:(?:[\w-]+\s+){0,4}(?:role|job)(?:\x27s)?\s+scope|scope\s+of\s+(?:[\w-]+\s+){0,4}(?:role|job)|what\s+(?:my|the|that|this)\s+(?:role|job)\s+covered))\b"
}


def review(value,application_id,relative,fact_ids=()):
    root=ws.checked_root(value);state=ws.load(root)
    app=next((a for a in state['applications'] if a['id']==application_id),None);ws.require(app is not None,'Unknown application.')
    ws.require(relative.startswith(('scratch/','applications/'+application_id+'/')),'Review a scratch draft or this application\'s pack.')
    path=ws.inside(root,relative);ws.require(path.suffix.lower() in ('.md','.txt'),'Review plain-text Markdown or text.')
    text=path.read_text(encoding='utf-8-sig');before=ws.digest(path)
    facts={f['id']:f for f in state['profile']['facts']};ws.require(all(fid in facts for fid in fact_ids),'Unknown evidence fact ID.')
    flags=[]
    for number,line in enumerate(text.splitlines(),1):
        normalized=line.replace('’',"'")
        for kind,pattern in PATTERNS.items():
            if re.search(pattern,normalized,re.I):flags.append({'line':number,'kind':kind,'text':line})
        if not app.get('submission') and re.search(r'\bsubmitted\s+(?:resume|cv|letter|materials)\b',normalized,re.I):
            flags.append({'line':number,'kind':'unverified_submission_label','text':line})
    ws.require(ws.digest(path)==before,'Draft changed during review; scan its current version.')
    return {'file':relative,'sha256':before,'status':'review_required' if flags else 'no_phrase_flags','flags':flags,
            'evidence':[{'id':fid,'claim':facts[fid]['claim'],'limits':facts[fid]['limits'],'status':facts[fid]['status'],'source_ids':facts[fid]['source_ids']} for fid in dict.fromkeys(fact_ids)],
            'limitation':'Limited English phrase scan. Questions, quoted source text and supported claims can be flagged; paraphrases can be missed. Flags are not proof of falsehood and a clear scan is not approval.',
            'next_action':'Read each flagged line against the actual candidate source. Remove unsupported self-claims; retain precise scope. Save a short resolution for justified wording. Also check promised sections, headings and the proposed chat summary. Rescan after meaningful edits, not repeatedly without changes.'}


def main():
    ws.configure_output();p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True);p.add_argument('--application',required=True);p.add_argument('--file',required=True);p.add_argument('--fact-id',action='append',default=[]);a=p.parse_args()
    try:print(json.dumps(review(a.workspace,a.application,a.file,a.fact_id),ensure_ascii=False,indent=2));return 0
    except (ws.WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:print('Stage review refused: '+str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
