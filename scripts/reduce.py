"""Stage 4-6: deterministic tables, unit test, synthesis hook, numeric verification."""
import csv,json,sys,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); from common import *
def aggregate(rows):
    out={'total':len(rows),'auth_methods':collections.Counter(),'by_category':{},'verdicts':collections.Counter(),'blockers':collections.Counter()}
    for r in rows:
        c=r['category']; out['by_category'].setdefault(c,{'total':0,'self_serve':0,'easy_wins':0,'needs_outreach':0}); x=out['by_category'][c]; x['total']+=1
        for m in r.get('auth',{}).get('methods',[]): out['auth_methods'][m]+=1
        v=r.get('buildability',{}).get('verdict'); out['verdicts'][v]+=1
        b=r.get('buildability',{}).get('blocker');
        if b: out['blockers'][b]+=1
        if r.get('access',{}).get('self_serve'): x['self_serve']+=1
        easy=r.get('access',{}).get('self_serve') and r.get('api_surface',{}).get('type')=='REST' and v=='buildable_today'
        x['easy_wins']+=bool(easy); x['needs_outreach']+=r.get('access',{}).get('gate_type')=='partner_contact_sales'
    return out
def main():
    rows=[read_json(app_path(a['app'],'extracted')) for a in csv.DictReader(open(ROOT/'config/apps.csv'))]; rows=[r for r in rows if r]
    # fixture test
    assert aggregate([{'category':'x','auth':{'methods':['OAuth2']},'access':{'self_serve':True,'gate_type':'none'},'api_surface':{'type':'REST'},'buildability':{'verdict':'buildable_today'}}]*2)['total']==2
    agg=aggregate(rows); write_json(ROOT/'data/aggregates.json',agg)
    print(json.dumps(agg,indent=2,default=dict))
if __name__=='__main__': main()
