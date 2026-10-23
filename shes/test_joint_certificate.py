import unittest, random, math
def check(tp,tb,dp,db,limp,limb,margin):
    return all(math.isfinite(x) for x in (tp,tb,dp,db)) and tp+dp<=limp and tb+db<=limb and tb-(tp+dp)>=margin
def dwell(intervals,pickup,required,deadline):
    timer=0.0
    for start,end,current in intervals:
        if start>=deadline: break
        duration=max(0,min(end,deadline)-start)
        timer=timer+duration if current>pickup else 0.0
        if timer+1e-12>=required: return True
    return False
class JointTests(unittest.TestCase):
    def test_breaker_delay(self):
        self.assertFalse(check(.20,.30,.12,.01,.5,.8,.05))
        self.assertTrue(check(.20,.30,.02,.01,.5,.8,.05))
    def test_backup_deadline(self):
        self.assertFalse(check(.1,.3,.01,.6,.5,.8,.05))
    def test_strict_pickup(self):
        self.assertFalse(dwell([(0,.3,1.)],1.,.1,.3))
    def test_disjoint_pulses(self):
        self.assertFalse(dwell([(0,.06,2.),(.06,.12,.5),(.12,.18,2.)],1.,.1,.18))
    def test_deadline_equality(self):
        self.assertTrue(dwell([(0,.1,2.)],1.,.1,.1))
    def test_randomized_oracle(self):
        rng=random.Random(20261023)
        for _ in range(10000):
            tp,tb,dp,db,limp,limb,margin=[rng.uniform(0,1) for _ in range(7)]
            self.assertEqual(check(tp,tb,dp,db,limp,limb,margin),tp+dp<=limp and tb+db<=limb and tb>=tp+dp+margin)
if __name__=='__main__': unittest.main()
