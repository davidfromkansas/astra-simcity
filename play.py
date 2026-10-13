#!/usr/bin/env python3
"""One logged, reviewable game action. Decisions and results are public."""
import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'bridge'))
from controller import Client
from telemetry import event,sample,export,snapshot
if __name__=='__main__':
 action=sys.argv[1];args=json.loads(sys.argv[2]);reason=sys.argv[3]
 event(reason,action=action,arguments=args)
 try:
  with Client() as c:
   if action=='sample':
    c.keypress('alt+s');c.advance(600);c.keypress('enter');c.advance(600);result=c.observe();value=sample();print(json.dumps({k:v for k,v in value.items() if k!='graphs'}));snapshot()
   else:result=getattr(c,action)(**args)
  event('Completed '+action,kind='action',action=action,arguments=args)
 except Exception as e:
  event(str(e),kind='error',action=action);raise
 finally:export()
 print(json.dumps(result))
