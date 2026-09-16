"""Stage 2: batch extraction. Replace llm_json() with the playground model call."""
import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); from common import *
SCHEMA='''{app,category,description,auth:{methods,primary},access:{self_serve,gate_type,notes},api_surface:{type,breadth,mcp_exists},buildability:{verdict,blocker},evidence:[{url,note,fetched_at}],confidence,grounding_pass,critic_agreement}'''

def llm_json(prompt): raise RuntimeError('Configure batched model adapter')
def batches(xs,n=9):
    for i in range(0,len(xs),n): yield xs[i:i+n]
def main():
    apps=list(csv.DictReader(open(ROOT/'config/apps.csv')))
    pending=[]
    for a in apps:
        if not app_path(a['app'],'extracted').exists():
            raw=read_json(app_path(a['app'],'raw')) or {'pages':[]}
            text='\n\n'.join(f"URL: {p.get('url')}\n{p.get('text','')}" for p in raw['pages'])[:24000]
            pending.append({'app':a,'text':text})
    for batch in batches(pending):
        prompt=f"Return ONLY a JSON array, one object per app, matching this schema: {SCHEMA}. Every populated claim must cite an evidence URL from supplied text. Apps: {json.dumps(batch,ensure_ascii=False)}"
        for obj in llm_json(prompt): write_json(app_path(obj['app'],'extracted'),obj)
if __name__=='__main__': main()
