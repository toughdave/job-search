#!/usr/bin/env python3
"""Create clean, byte-identical upload copies from documented visual reviews."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
import workspace as ws


def clean(value):
    text=unicodedata.normalize('NFC',value)
    return ' '.join(''.join(c if c.isalnum() or unicodedata.category(c).startswith('M') or c in " -.'’" else ' ' for c in text).split()).strip(' -')


def filename(name,employer,role,kind,extension):
    ws.require(kind in ('resume','cv','cover_letter'),'Choose resume, cv or cover_letter.')
    ws.require(extension in ('.pdf','.docx'),'Only reviewed PDF or DOCX uploads are supported.')
    def without_parentheses(value):
        while re.search(r'\([^()]*\)',value):value=re.sub(r'\([^()]*\)',' ',value)
        return clean(value)
    parts=[clean(name),without_parentheses(employer),without_parentheses(role)]
    ws.require(all(parts),'Name, employer and role must contain usable filename characters.')
    label={'resume':'Resume','cv':'CV','cover_letter':'Cover Letter'}[kind]
    suffix=' - '+label+extension
    # Identity is never shortened or silently sanitized. Request an explicitly
    # supported filename name if it cannot be represented safely within the limit.
    ws.require(parts[0]==' '.join(unicodedata.normalize('NFC',name).split()),'Name contains unsafe filename characters; confirm a supported filename name instead of changing it automatically.')
    def joined():return ' - '.join(p for p in parts if p)+suffix
    def fits():return len(joined())<=80 and len(joined().encode('utf-8'))<=255
    employer_full=parts[1]
    # Preserve the entire role instead of guessing its head noun across languages.
    # Employer words can be shortened or omitted first, including one long word.
    while not fits() and parts[1]:
        parts[1]=parts[1].rsplit(' ',1)[0] if ' ' in parts[1] else ''
    if not fits():
        # A role that cannot fit even alone is omitted whole, never reduced to
        # misleading fragments such as Senior, Dental or IT. Restore the employer.
        parts[2]='';parts[1]=employer_full
        while not fits() and parts[1]:
            parts[1]=parts[1].rsplit(' ',1)[0] if ' ' in parts[1] else ''
    ws.require(fits(),'Full name and document label exceed the filename limit; ask for an explicitly approved shorter filename name. Never generate initials automatically.')
    return joined()


def prepare(value,application_id,source,review_file,name,name_fact_id,kind):
    root=ws.checked_root(value)
    with ws.write_lock(root):
        state=ws.load(root);application=next((a for a in state['applications'] if a['id']==application_id),None)
        ws.require(application is not None,'Unknown application.')
        fact=next((f for f in state['profile']['facts'] if f['id']==name_fact_id),None)
        ws.require(fact and fact['category']=='identity' and fact['status'] in ('verified','candidate_reported'),'Use a current supported identity fact for the name.')
        ws.require(clean(name).casefold() and re.search(r'(?<!\w)'+re.escape(clean(name).casefold())+r'(?!\w)',clean(fact['claim']).casefold()),'The supplied name is not present in the linked identity claim.')
        src=ws.inside(root,source);review_path=ws.inside(root,review_file)
        ws.require(source.startswith(('documents/','applications/')),'Source must be a private document or application artifact.')
        if source.startswith('applications/'):
            ws.require(source.startswith('applications/'+application_id+'/'),'Source belongs to a different application.')
        ws.require(src.is_file(),'Reviewed source file is missing.')
        review_bytes=review_path.read_bytes();review_hash=hashlib.sha256(review_bytes).hexdigest()
        review=json.loads(review_bytes.decode('utf-8-sig'))
        ws.require(review.get('file')==source and review.get('sha256')==ws.digest(src),'Visual review does not match the current source bytes.')
        count=review.get('page_count');pages=review.get('pages_inspected')
        ws.require(type(count) is int and 0<count<=1000 and isinstance(pages,list) and all(type(p) is int for p in pages) and sorted(pages)==list(range(1,count+1)),'Visual review must cover every page exactly once.')
        ws.require(review.get('status')=='reviewed' and review.get('unresolved_defects')==[] and isinstance(review.get('renderer'),str) and review['renderer'].strip() and isinstance(review.get('findings'),str) and review['findings'].strip(),'Complete the actual visual review and its findings first.')
        ws.stamp(review.get('reviewed_at'),'reviewed_at')
        basename=filename(name,application['employer'],application['role'],kind,src.suffix.lower())
        relative='applications/'+application_id+'/uploads/'+review['sha256'][:16]+'/'+basename
        result=ws.import_file(root,src,relative)
        ws.require(result['sha256']==review['sha256'],'Source changed while making upload copy; do not upload this copy. Review the current source again.')
        ws.require(ws.digest(review_path)==review_hash,'Review record changed; inspect it again before upload.')
        return {**result,'basename':basename,'markdown_link':'['+basename+'](<'+ws.inside(root,relative).as_posix()+'>)','review':{'file':review_file,'sha256':review_hash},'reviewed_source':source,
                'next_action':'Record this upload copy and review reference in the application. Recheck its hash before upload. This validates a review record, not the act of viewing pages.'}


def main():
    ws.configure_output();p=argparse.ArgumentParser(description=__doc__)
    for flag in ('workspace','application','source','review','name','name-fact-id','kind'):p.add_argument('--'+flag,required=True)
    a=p.parse_args()
    try:print(json.dumps(prepare(a.workspace,a.application,a.source,a.review,a.name,a.name_fact_id,a.kind),ensure_ascii=False,indent=2));return 0
    except (ws.WorkspaceError,OSError,ValueError,KeyError,TypeError) as e:print('Upload copy not ready: '+str(e),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
