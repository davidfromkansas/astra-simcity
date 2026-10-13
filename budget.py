"""Record a budget only after visually reading its year-end screen."""
import sys,time,shutil,json
from telemetry import ROOT,append,event,snapshot,export,read

def score(state,settlement,profit,qualifies):
 state=dict(state)
 if qualifies:
  if not state.get('population_met_year') or settlement-1<=state['population_met_year']:
   raise ValueError('Not a full year after the population milestone')
  prior=state.get('last_qualifying_year')
  if prior is not None and settlement-1<=prior:raise ValueError('Budget year already scored')
  state['profit_streak']=(state.get('profit_streak',0)+1 if prior==settlement-2 else 1) if profit>0 else 0
  state['last_qualifying_year']=settlement-1
  if state['profit_streak']>=3:state.update(status='Challenge completed · three profitable years',completed_at=time.time())
 return state

if __name__=='__main__':
 settlement,income,expenses,profit=map(int,sys.argv[1:5]);qualifies=len(sys.argv)>5 and sys.argv[5]=='qualifies'
 if any(b['settlement_year']==settlement for b in read('budgets.jsonl')):raise ValueError('Budget already recorded')
 if qualifies and any(s['metrics']['bonds'] for s in read('samples.jsonl')):raise ValueError('Borrowing violates this challenge')
 state=score(json.loads((ROOT/'challenge.json').read_text()),settlement,profit,qualifies)
 evidence=f'screenshots/budget-{settlement}.png';shutil.copyfile(ROOT.parent/'bridge/live-frame.png',ROOT/'docs'/evidence)
 append('budgets.jsonl',dict(year=settlement-1,settlement_year=settlement,income=income,expenses=expenses,profit=profit,source=f'January {settlement} year-end budget screen; displayed rows may be rounded',evidence=evidence,time=time.time(),qualifies=qualifies))
 event(f'Annual budget settling January {settlement}: ${income} income, ${expenses} operating spending, ${profit} displayed surplus. '+('Counts toward the post-target streak.' if qualifies else 'Before the first full post-target year; does not count toward the streak.'))
 (ROOT/'challenge.json').write_text(json.dumps(state));snapshot();export()
