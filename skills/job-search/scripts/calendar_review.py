"""Check explicit English weekday/date pairs without guessing a missing year."""
import re
from datetime import date
import workspace as ws

DAYS=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
MONTHS=('January','February','March','April','May','June','July','August','September','October','November','December')
WEEKDAY=r'(?:Mon(?:day)?|Tue(?:s(?:day)?)?|Wed(?:nesday)?|Thu(?:rs?(?:day)?)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)'
MONTH=r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
PAIR=re.compile(r'\b(?P<weekday>'+WEEKDAY+r')\b\.?(?:\s*,\s*|\s+|(?=\())(?:\(\s*)?(?:the\s+)?(?:(?P<month>'+MONTH+r')\b\.?\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?|(?P<day_first>\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?(?P<month_last>'+MONTH+r')\b\.?)(?:(?:\s*,\s*|\s+)(?P<year>\d{4})\b)?\)?',re.I)


def scan(text):
    flags=[]
    for match in PAIR.finditer(text):
        # Lowercase short forms can be ordinary words: "exam sat", "we wed".
        # Full weekday names and capitalized abbreviations remain recognized.
        if match['weekday'] in ('sat','wed','sun','mon'):continue
        item={'line':text.count('\n',0,match.start())+1,'text':match.group()}
        if not match['year']:
            flags.append({**item,'kind':'calendar_year_missing','severity':'review','message':'Confirm the year from saved context before relying on the weekday; no year was assumed.'})
            continue
        month=(match['month'] or match['month_last'])[:3].lower()
        month=next(i for i,name in enumerate(MONTHS,1) if name[:3].lower()==month)
        try:actual=date(int(match['year']),month,int(match['day'] or match['day_first']))
        except ValueError:
            flags.append({**item,'kind':'calendar_invalid_date','severity':'error','message':'This calendar date does not exist.'});continue
        expected=DAYS[actual.weekday()]
        if match['weekday'][:3].lower()!=expected[:3].lower():
            flags.append({**item,'kind':'calendar_weekday_mismatch','severity':'error','expected_weekday':expected,'date':actual.isoformat(),'message':'Weekday/date mismatch: '+actual.isoformat()+' is '+expected+'. Correct the active text; a disclaimer does not fix it.'})
    return flags


def check(text):
    flags=scan(text)
    errors=[f for f in flags if f['severity']=='error']
    ws.require(not errors,'Calendar review: '+' '.join(f['message'] for f in errors))
    return flags
