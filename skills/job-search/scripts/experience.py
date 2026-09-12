"""Employer/role-period evidence and candidate-confirmed work-history coverage."""
import workspace as ws


def validate(state):
    ob=state['onboarding']
    entries=ws.indexed(ob.get('experiences',[]),'experiences')
    facts=ws.indexed(state['profile']['facts'],'facts')
    sources=ws.indexed(state['sources'],'sources')
    answers=ws.indexed(state['interviews'],'interviews')
    replaced=set()
    for entry in entries.values():
        for field in ('employer','role','start','end'):
            ws.require(isinstance(entry.get(field),str) and entry[field].strip(),f'Experience {field} required; preserve reported date precision or record unknown.')
        ws.require(entry.get('kind') in ('employment','self_employment','volunteering','project','education'),'Experience kind required.')
        ws.refs(entry.get('source_ids'),sources,'Experience')
        ws.refs(entry.get('fact_ids'),facts,'Experience facts')
        ws.require(all(set(facts[f]['source_ids']).intersection(entry['source_ids']) for f in entry['fact_ids']),'Experience sources must support its facts.')
        old=entry.get('supersedes')
        if old is not None:
            ws.require(old in entries and old!=entry['id'] and old not in replaced,'Experience correction must replace one known entry once.')
            replaced.add(old)
    for entry in entries.values():
        seen=set();cursor=entry
        while cursor.get('supersedes'):
            ws.require(cursor['id'] not in seen,'Experience correction cycle.')
            seen.add(cursor['id']);cursor=entries[cursor['supersedes']]
    for fact in facts.values():
        if fact.get('experience_id') is not None:
            ws.require(fact['experience_id'] in entries,'Fact experience missing.')
    topics=ws.indexed(ob['topics'],'topics')
    for topic in topics.values():
        if topic.get('experience_id') is not None:
            ws.require(topic['experience_id'] in entries,'Topic experience missing.')
    for ev in ob['evidence']:
        eid=topics[ev['topic_id']].get('experience_id')
        if eid is None:continue
        ws.require(all(facts[f].get('experience_id')==eid or f in entries[eid]['fact_ids'] for f in ev['fact_ids']),'Evidence belongs to a different employer/role period.')
        for aid in ev.get('answer_ids',[]):
            answer=answers[aid];qid=answer.get('onboarding_question_id')
            if qid:
                question=next(q for q in ob['questions'] if q['id']==qid)
                ws.require(topics[question['topic_id']].get('experience_id')==eid,'Answer belongs to a different employer/role period.')
    for review in ws.indexed(ob.get('history_reviews',[]),'history reviews').values():
        ws.require(review.get('status') in ('complete','more_to_add'),'History review status required.')
        ws.refs(review.get('experience_ids'),entries,'History inventory',False)
        ws.refs(review.get('resume_source_ids'),sources,'Reviewed resume sources',False)
        ws.refs(review.get('source_ids'),sources,'History confirmation')
        aid=review.get('answer_id')
        ws.require(aid in answers,'History confirmation needs the exact saved answer.')
        ws.require(set(answers[aid]['source_ids']).intersection(review['source_ids']),'History confirmation must cite its answer source.')
        ws.require(any(sources[s]['kind'] in ('candidate_answer','candidate_report') for s in review['source_ids']),'Candidate must confirm the work-history inventory.')


def coverage(state,rows):
    ob=state['onboarding'];facts={f['id']:f for f in state['profile']['facts']}
    entries=ob.get('experiences',[])
    replaced={e['supersedes'] for e in entries if e.get('supersedes')}
    active=[e for e in entries if e['id'] not in replaced]
    reviews=ob.get('history_reviews',[]);review=reviews[-1] if reviews else None
    confirmed=bool(review and review['status']=='complete'
        and set(review['experience_ids'])=={e['id'] for e in active}
        and set(review['resume_source_ids'])==set(ob['resume'].get('source_ids',[])))
    resolved=('answered','declined','not_applicable','no_example')
    by_id={r['id']:r for r in rows};result=[]
    for entry in active:
        topics=[t for t in ob['topics'] if t.get('experience_id')==entry['id'] and t['id'] in by_id and t['required']]
        role=[t for t in topics if t['kind']=='profile' and 'responsibilities' in t['dimensions']]
        stories=[t for t in topics if t['kind']=='example' and t['track_id']==ob['active_track']]
        valid=all(facts[f]['status'] in ('candidate_reported','verified') for f in entry['fact_ids'])
        gaps=[]
        if not valid:gaps.append('reconcile_role_facts')
        if not role:gaps.append('add_responsibilities_topic')
        if not stories:gaps.append('add_employer_example_topic')
        gaps.extend(t['id'] for t in topics if by_id[t['id']]['status'] not in resolved)
        result.append({**entry,'resolved':not gaps,'gaps':gaps})
    return {'inventory_confirmed':confirmed,'experiences':result,
            'ready':confirmed and all(e['resolved'] for e in result),
            'instruction':'Reconcile this project resume and saved answers into separate employer/role periods. Confirm all employers have been listed. Review existing evidence before asking role-specific missing questions.'}
