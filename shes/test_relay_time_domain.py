import math, random, unittest
from relay_time_domain import (Segment, inverse_time_constant, relay_assertion,
 definite_time_assertion, coordinated)

class RelayModelTests(unittest.TestCase):
 def test_constant_current_exact(self):
  for current in (1.1,1.5,2.,5.,10.):
   t=inverse_time_constant(current,1.,.1)
   self.assertAlmostEqual(relay_assertion([Segment(0,2*t,current)],2*t,1.,.1),t,places=10)
 def test_strict_pickup(self):
  self.assertTrue(math.isinf(relay_assertion([Segment(0,10,1.)],10,1.,.1)))
 def test_full_reset_vs_hold(self):
  s=[Segment(0,.06,3.),Segment(.06,.08,0.),Segment(.08,.14,3.)]
  t=inverse_time_constant(3.,1.,.1)
  # choose pulses with each shorter than T, sum longer than T
  d=.75*t
  s=[Segment(0,d,3.),Segment(d,d+.01,0.),Segment(d+.01,2*d+.01,3.)]
  self.assertTrue(math.isinf(relay_assertion(s,2*d+.01,1.,.1,"full")))
  self.assertTrue(math.isfinite(relay_assertion(s,2*d+.01,1.,.1,"hold")))
 def test_linear_reset_between(self):
  t=inverse_time_constant(3.,1.,.1); d=.75*t
  s=[Segment(0,d,3.),Segment(d,d+.01,0.),Segment(d+.01,2*d+.01,3.)]
  hold=relay_assertion(s,2*d+.01,1.,.1,"hold")
  partial=relay_assertion(s,2*d+.01,1.,.1,"linear",reset_rate=10.)
  self.assertLessEqual(hold,partial)
 def test_definite_deadline_equality(self):
  self.assertAlmostEqual(definite_time_assertion([Segment(0,.1,2.)],.1,1.,.1),.1)
 def test_primary_breaker_delay_counterexample(self):
  self.assertFalse(coordinated(.2,.3,.12,.01,.5,.8,.05))
  self.assertTrue(coordinated(.2,.3,.02,.01,.5,.8,.05))
 def test_reject_gap(self):
  with self.assertRaises(ValueError):
   relay_assertion([Segment(0,.1,2.),Segment(.2,.3,2.)],.3,1.,.1)
 def test_reject_negative_current(self):
  with self.assertRaises(ValueError):
   relay_assertion([Segment(0,1,-1.)],1,1.,.1)
 def test_piecewise_oracle(self):
  rng=random.Random(20261023)
  for _ in range(10000):
   i=rng.uniform(1.01,5.); tds=rng.uniform(.01,.3)
   total=inverse_time_constant(i,1.,tds)
   a=rng.random()*total
   s=[Segment(0,a,i),Segment(a,2*total,i)]
   self.assertAlmostEqual(relay_assertion(s,2*total,1.,tds),total,places=9)
 def test_reset_monotonicity(self):
  rng=random.Random(2204)
  for _ in range(1000):
   current=rng.uniform(1.1,4.); t=inverse_time_constant(current,1.,.1)
   a=.7*t; b=.7*t
   s=[Segment(0,a,current),Segment(a,a+.02,0.),Segment(a+.02,a+.02+b,current)]
   h=relay_assertion(s,a+.02+b,1.,.1,"hold")
   f=relay_assertion(s,a+.02+b,1.,.1,"full")
   self.assertTrue(math.isfinite(h))
   self.assertTrue(math.isinf(f))
if __name__=="__main__": unittest.main()
