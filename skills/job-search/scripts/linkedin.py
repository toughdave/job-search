"""LinkedIn review freshness from this candidate's saved profile and evidence."""
from urllib.parse import urlsplit
import workspace as ws


def relevant_facts(state):
    return sorted(f['id'] for f in state['profile']['facts']
                  if f['status'] in ('verified', 'candidate_reported') and f['category'] != 'preference')


def validate(state, root):
    cfg = state['integrations'].get('linkedin')
    if cfg is None:
        return
    ws.require(isinstance(cfg, dict) and cfg.get('version') == 1, 'Unknown LinkedIn record format.')
    facts = ws.indexed(state['profile']['facts'], 'facts')
    sources = ws.indexed(state['sources'], 'sources')
    ws.require(cfg.get('profile_fact_id') in facts, 'LinkedIn URL needs a saved candidate fact.')
    url = cfg.get('url')
    ws.require(isinstance(url, str), 'LinkedIn URL required.')
    parsed = urlsplit(url)
    host = (parsed.hostname or '').lower()
    ws.require(parsed.scheme == 'https' and not parsed.username and not parsed.password
               and (host == 'linkedin.com' or host.endswith('.linkedin.com'))
               and parsed.path.startswith('/in/') and len(parsed.path.strip('/').split('/')) == 2,
               'Use the candidate-provided HTTPS LinkedIn /in/ profile URL.')
    ws.refs(cfg.get('profile_source_ids', []), sources, 'LinkedIn profile content', nonempty=False)
    tracks = ws.indexed(state.get('onboarding', {}).get('tracks', []), 'tracks')
    for review in ws.indexed(cfg.get('reviews', []), 'LinkedIn reviews').values():
        ws.require(review.get('track_id') in tracks, 'LinkedIn review needs its occupation scope.')
        ws.require(review.get('profile_fact_id') in facts, 'LinkedIn review URL fact missing.')
        ws.refs(review.get('profile_source_ids'), sources, 'Reviewed LinkedIn content')
        ws.refs(review.get('fact_ids'), facts, 'LinkedIn review evidence')
        ws.stamp(review.get('reviewed_at'), 'LinkedIn review time')
        ws.file_ref(root, review.get('output'), 'LinkedIn review draft')


def guard_history(old, new):
    before = old['integrations'].get('linkedin')
    if before is None:
        return
    after = new['integrations'].get('linkedin')
    ws.require(after is not None, 'Preserve saved LinkedIn records; record a decline instead of deleting history.')
    prior = before.get('reviews', [])
    ws.require(after.get('reviews', [])[:len(prior)] == prior, 'LinkedIn review history is append-only.')


def plan(state):
    cfg = state['integrations'].get('linkedin')
    result = {'status': 'link_not_recorded', 'review_grants_publication_permission': False}
    if cfg is None:
        return result
    facts = ws.indexed(state['profile']['facts'], 'facts')
    if facts[cfg['profile_fact_id']]['status'] not in ('verified', 'candidate_reported'):
        return {**result, 'status': 'profile_link_needs_confirmation'}
    current = relevant_facts(state)
    unresolved = [f['id'] for f in state['profile']['facts'] if f['status'] == 'unresolved' and f['category'] != 'preference']
    result.update(url=cfg['url'], fact_ids=current, unresolved_fact_ids=unresolved)
    if not cfg.get('profile_source_ids'):
        return {**result, 'status': 'profile_content_not_read'}
    last = cfg.get('reviews', [])[-1] if cfg.get('reviews') else None
    if not last:
        return {**result, 'status': 'review_not_recorded'}
    reasons = []
    if last['profile_fact_id'] != cfg['profile_fact_id']:
        reasons.append('profile_link_changed')
    if set(last['profile_source_ids']) != set(cfg['profile_source_ids']):
        reasons.append('profile_content_changed')
    if last['track_id'] != state['onboarding']['active_track']:
        reasons.append('occupation_changed')
    if set(last['fact_ids']) != set(current):
        reasons.append('career_evidence_changed')
    if unresolved:
        reasons.append('unresolved_career_evidence')
    return {**result, 'status': 'review_needs_refresh' if reasons else 'review_current',
            'review_id': last['id'], 'reasons': reasons,
            'instruction': 'Check the saved review choice and any deferral before acting. This compares saved records only; it does not prove the live profile is unchanged or authorize publication.'}
