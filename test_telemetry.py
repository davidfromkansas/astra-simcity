import unittest,tempfile,struct,json
from pathlib import Path
from metrics import decode,parse
ROOT=Path(__file__).resolve().parent
class TelemetryTests(unittest.TestCase):
 def test_rle(self):
  self.assertEqual(decode(bytes([3,1,2,3,130,7])),bytes([1,2,3,7,7,7]))
  with self.assertRaises(ValueError):decode(bytes([3,1]))
 def test_incomplete_save_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'partial.SC2';p.write_bytes(b'FORM\0\0\0\0SCDHgarbage')
   with self.assertRaises(ValueError):parse(p)
 def test_verified_starting_observation(self):
  s=json.loads((ROOT/'samples.jsonl').read_text().splitlines()[0])
  self.assertEqual((s['year'],s['month'],s['metrics']['funds'],s['metrics']['population'],s['metrics']['bonds']),(1900,1,20000,0,0))
 def test_public_data_paths_exist(self):
  d=json.loads((ROOT/'docs/data.json').read_text())
  for shot in d['timeline']:
   p=(ROOT/'docs'/shot['image']).resolve();self.assertTrue(str(p).startswith(str((ROOT/'docs/screenshots').resolve())+'/'));self.assertTrue(p.exists())
  self.assertTrue(all(s['metrics']['bonds']==0 for s in d['samples']))
class ScoringTests(unittest.TestCase):
 def test_full_consecutive_years(self):
  from budget import score
  state={'population_met_year':1907}
  with self.assertRaises(ValueError):score(state,1908,10,True)
  for year in (1909,1910,1911):state=score(state,year,10,True)
  self.assertEqual(state['profit_streak'],3)
  self.assertIn('completed_at',state)
  with self.assertRaises(ValueError):score(state,1911,10,True)
 def test_gap_or_loss_resets_streak(self):
  from budget import score
  s=score({'population_met_year':1907},1909,10,True)
  s=score(s,1911,10,True);self.assertEqual(s['profit_streak'],1)
  s=score(s,1912,-1,True);self.assertEqual(s['profit_streak'],0)
if __name__=='__main__':unittest.main()
