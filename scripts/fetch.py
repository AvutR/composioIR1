"""Stage 1: resumable candidate discovery/fetch through Composio Search tools.
The adapter is intentionally isolated so the same pipeline can run in the playground
or from a worker that exposes COMPOSIO_SEARCH_WEB/FETCH_URL_CONTENT.
"""
import csv, asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); from common import *

# Implement these two functions with your playground's Composio tool runner.
# In the Tool Router playground, map them to COMPOSIO_SEARCH_WEB and
# COMPOSIO_SEARCH_FETCH_URL_CONTENT respectively.
def composio_search(query): raise RuntimeError('Configure Composio adapter: COMPOSIO_SEARCH_WEB')
def composio_fetch(urls): raise RuntimeError('Configure Composio adapter: COMPOSIO_SEARCH_FETCH_URL_CONTENT')

def candidates(hint):
    from urllib.parse import urlparse
    p=urlparse(hint); base=f'{p.scheme}://{p.netloc}'
    return list(dict.fromkeys([hint,base]+[base+x for x in ['/auth','/authentication','/api-reference','/docs','/pricing','/developers']]))

async def main():
    apps=list(csv.DictReader(open(ROOT/'config/apps.csv')))
    if len(apps)!=100: raise SystemExit(f'Expected exactly 100 apps, found {len(apps)}')
    sem=asyncio.Semaphore(int(os.getenv('CONCURRENCY','18')))
    async def one(a):
        p=app_path(a['app'],'raw')
        if p.exists(): return a['app'],'cached'
        async with sem:
            urls=candidates(a['hint_url'])
            try: pages=composio_fetch(urls)
            except Exception as e: pages={'error':str(e),'pages':[]}
            usable=[x for x in pages.get('pages',[]) if x.get('status',200)==200 and len(x.get('text','').strip())>200]
            if not usable:
                try:
                    s=composio_search(f"{a['app']} API authentication developer docs")
                    hits=(s.get('citations') or s.get('results',{}).get('citations',[]))[:3]
                    pages2=composio_fetch([h.get('url',h) if isinstance(h,dict) else h for h in hits])
                    usable += [x for x in pages2.get('pages',[]) if len(x.get('text','').strip())>200]
                except Exception as e: pages['fallback_error']=str(e)
            write_json(p,{'app':a,'fetched_at':NOW(),'pages':usable,'zero_usable':not bool(usable)})
            return a['app'],'fetched' if usable else 'zero'
    print(await asyncio.gather(*(one(a) for a in apps)))
if __name__=='__main__': asyncio.run(main())
