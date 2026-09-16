from pathlib import Path
import json, os, re, hashlib
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw'; EXTRACTED=ROOT/'data/extracted'; OUTPUT=ROOT/'output'
NOW=lambda: datetime.now(timezone.utc).isoformat()

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
def read_json(p): return json.loads(Path(p).read_text()) if Path(p).exists() else None
def write_json(p,obj):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False))
def app_path(app,kind): return (RAW if kind=='raw' else EXTRACTED)/(slug(app)+'.json')
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
