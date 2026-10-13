import json,time,os,shutil
from pathlib import Path
from metrics import parse
ROOT=Path(__file__).resolve().parent;DOCS=ROOT/'docs';BRIDGE=ROOT.parent/'bridge'
def append(name,value):
 with (ROOT/name).open('a') as f:f.write(json.dumps(value,separators=(',',':'))+'\n')
def read(name):
 p=ROOT/name
 if not p.exists():return []
 result=[]
 for line in p.read_text().splitlines():
  try:result.append(json.loads(line))
  except ValueError:pass
 return result
def event(message,kind='decision',**kw):append('events.jsonl',dict(time=time.time(),kind=kind,message=message,**kw))
def sample():
 value=parse(BRIDGE/'game/ASTRALAB.SC2');previous=read('samples.jsonl')
 if not previous or value['sha256']!=previous[-1]['sha256']:append('samples.jsonl',value)
 return value
def snapshot():
 now=time.time();out=DOCS/'screenshots'/f'{int(now)}.png';out.parent.mkdir(exist_ok=True);shutil.copyfile(BRIDGE/'live-frame.png',out)
 append('timeline.jsonl',{'time':now,'image':'screenshots/'+out.name})
def export():
 DOCS.mkdir(exist_ok=True);samples=read('samples.jsonl');state=json.loads((ROOT/'challenge.json').read_text())
 recording=json.loads((BRIDGE/'recordings/session.json').read_text()) if (BRIDGE/'recordings/session.json').exists() else {}
 data=dict(updated_at=time.time(),challenge=state,samples=samples,timeline=read('timeline.jsonl'),events=read('events.jsonl'),recording={'status':recording.get('status'),'audio':False},budgets=read('budgets.jsonl'))
 tmp=DOCS/'data.tmp';tmp.write_text(json.dumps(data,separators=(',',':')));os.replace(tmp,DOCS/'data.json')
 shutil.copyfile(BRIDGE/'live-frame.png',DOCS/'latest.png')
if __name__=='__main__':
 import sys
 if len(sys.argv)>1 and sys.argv[1]=='sample':sample()
 export()
