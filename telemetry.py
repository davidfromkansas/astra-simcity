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
 state=json.loads((ROOT/'challenge.json').read_text())
 if value['metrics']['population']>=2000 and value['year']<1910 and not state.get('population_met_at'):
  state.update(population_met_at=value['time'],population_met_year=value['year'],population_met_age=value['age'],status='Population target reached · verifying profitable years')
  (ROOT/'challenge.json').write_text(json.dumps(state));event('Population target reached: '+str(value['metrics']['population'])+' residents in '+str(value['month'])+'/'+str(value['year'])+'. Next: three full profitable years without borrowing.',kind='milestone')
 return value
def snapshot():
 now=time.time();out=DOCS/'screenshots'/f'{int(now)}.png';out.parent.mkdir(exist_ok=True);shutil.copyfile(BRIDGE/'live-frame.png',out)
 append('timeline.jsonl',{'time':now,'image':'screenshots/'+out.name})
def export():
 DOCS.mkdir(exist_ok=True);samples=read('samples.jsonl');state=json.loads((ROOT/'challenge.json').read_text())
 recording=json.loads((BRIDGE/'recordings/session.json').read_text()) if (BRIDGE/'recordings/session.json').exists() else {}
 budgets=read('budgets.jsonl')
 for entry in samples:
  matching=[b for b in budgets if b['year']==entry['year']-1]
  if matching:
   b=matching[-1];entry['metrics'].update(annual_income=b['income'],annual_expenses=b['expenses'],annual_profit=b.get('profit',b['income']-b['expenses']))
 data=dict(updated_at=time.time(),challenge=state,samples=samples,timeline=read('timeline.jsonl'),events=read('events.jsonl'),recording={'status':recording.get('status'),'audio':False},budgets=read('budgets.jsonl'))
 tmp=DOCS/'data.tmp';tmp.write_text(json.dumps(data,separators=(',',':')));os.replace(tmp,DOCS/'data.json')
 shutil.copyfile(BRIDGE/'live-frame.png',DOCS/'latest.png')
if __name__=='__main__':
 import sys
 if len(sys.argv)>1 and sys.argv[1]=='sample':sample()
 export()
