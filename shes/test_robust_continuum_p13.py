import unittest,random,math
from shes.relay_time_domain import Segment,coordinated
from shes.robust_continuum_p13 import time_at_gamma,rectangular_certificate,correlated_counterexample
class ContinuumP13(unittest.TestCase):
 def test_interior_correlated_counterexample(self):
  w=correlated_counterexample()
  self.assertEqual([r["passes_margin_0_4"] for r in w["samples"]],[True,False,True])
  self.assertGreater(w["samples"][1]["primary_assert_s"],0)
 def test_monotonicity_all_reset_semantics(self):
  rng=random.Random(1313)
  for reset in ("full","hold","linear"):
   for _ in range(100):
    vals=[rng.uniform(.2,3.) for j in range(3)]
    tr=[Segment(0.,1.,vals[0]),Segment(1.,2.,vals[1]),Segment(2.,10.,vals[2])]
    times=[time_at_gamma(tr,g,.7,.04,reset) for g in (.5,.65,.8,1.,1.2)]
    self.assertTrue(all(a>=b for a,b in zip(times,times[1:])),(reset,times))
 def test_rectangle_vs_512_interior_samples(self):
  rng=random.Random(1314)
  for reset in ("full","hold","linear"):
   for _ in range(40):
    p=[Segment(0.,.2,2.),Segment(.2,.45,.2),Segment(.45,6.,2.)]
    b=[Segment(0.,.2,1.8),Segment(.2,.45,.18),Segment(.45,6.,1.8)]
    pp=rng.uniform(.3,.9);pb=rng.uniform(.3,.9)
    tp=rng.uniform(.02,.08);tb=rng.uniform(.08,.22)
    gpi=(.6,1.);gbi=(.6,1.);bpi=(0.,.08);bbi=(0.,.08)
    dp=2.;db=5.;margin=.1
    verdict=rectangular_certificate(p,b,pp,pb,tp,tb,gpi,gbi,bpi,bbi,dp,db,margin,reset)
    # Endpoint enumeration is independently checked, and samples cannot
    # contradict an approved exact rectangle certificate.
    for gp in (.6,.8,1.):
     for gb in (.6,.8,1.):
      for bp in (0.,.04,.08):
       for bb in (0.,.04,.08):
        ap=time_at_gamma(p,gp,pp,tp,reset)
        ab=time_at_gamma(b,gb,pb,tb,reset)
        ok=coordinated(ap,ab,bp,bb,dp,db,margin)
        if verdict:self.assertTrue(ok)
    # Converse only if independent rectangle corners pass (exact theorem).
    corner_ok=True
    for gp in gpi:
     for gb in gbi:
      for bp in bpi:
       for bb in bbi:
        ap=time_at_gamma(p,gp,pp,tp,reset)
        ab=time_at_gamma(b,gb,pb,tb,reset)
        corner_ok &= coordinated(ap,ab,bp,bb,dp,db,margin)
    self.assertEqual(verdict,corner_ok)
 def test_invalid_uncertainty(self):
  p=[Segment(0,5,1)]
  with self.assertRaises(ValueError):
   rectangular_certificate(p,p,.5,.5,.1,.1,(1.,.6),(.6,1),(0,.1),(0,.1),5,5,.1)
if __name__=="__main__":unittest.main()
