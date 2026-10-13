#!/usr/bin/env python3
"""Publish only the dashboard repo, every five minutes, for a bounded session."""
import time,subprocess,json,os
from pathlib import Path
from telemetry import export
ROOT=Path(__file__).resolve().parent
(ROOT/'publisher-session.json').write_text(json.dumps({'pid':os.getpid(),'started_at':time.time(),'interval_seconds':300,'maximum_hours':4}))
for i in range(48):
 try:
  export()
  subprocess.run(['git','add','docs','events.jsonl','samples.jsonl','timeline.jsonl','challenge.json'],cwd=ROOT,check=True)
  if subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode:
   subprocess.run(['git','commit','-m','Update city observations '+time.strftime('%Y-%m-%d %H:%M')],cwd=ROOT,check=True)
  subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True,timeout=60)
  print('Published',time.time(),flush=True)
 except Exception as e:print(type(e).__name__,str(e),flush=True)
 time.sleep(300)
