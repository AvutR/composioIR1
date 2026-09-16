"""Stage 3: deterministic grounding plus batched critic hook and spot-check ledger."""
import csv,re,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); from common import *
KEYS=['oauth','api key','basic','bearer','token','contact sales','mcp','graphql','rest','pricing']
def main():
    for a in csv.DictReader(open(ROOT/'config/apps.csv')):
        obj=read_json(app_path(a['app'],'extracted')); raw=read_json(app_path(a['app'],'raw')) or {}
        hay=' '.join(p.get('text','').lower() for p in raw.get('pages',[]))
        claims=json.dumps(obj or {}).lower()
        terms=[k for k in KEYS if k in claims and k not in ('rest',)]
        obj['grounding_pass']=all(t in hay for t in terms) if obj else False
        obj.setdefault('critic_agreement',None)
        if obj: write_json(app_path(a['app'],'extracted'),obj)
    write_json(ROOT/'data/spot_checks.json',{'instructions':'Record 15-20 manually reviewed rows with before/after correctness counts.','checks':[]})
if __name__=='__main__': main()
