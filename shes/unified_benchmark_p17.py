"""P17 controlled synthetic protection benchmark. No field/EMT inference."""
import json,random,time,math,argparse,pathlib
from shes.relay_time_domain import Segment,coordinated
from shes.robust_continuum_p13 import time_at_gamma,rectangular_certificate,correlated_counterexample

def frequency_ok(c):
 # Stipulated sign-aware frequency envelope, units Hz: f0 - df >= floor.
 return c["f0_hz"]-c["df_hz"]>=c["floor_hz"]

def params(c):
 return (c["primary"],c["backup"],c["pp"],c["pb"],c["tp"],c["tb"])
def evaluate(c,gp,gb,dp,db):
 p,b,pp,pb,tp,tb=params(c)
 return frequency_ok(c) and coordinated(time_at_gamma(p,gp,pp,tp,c["reset"]),
 time_at_gamma(b,gb,pb,tb,c["reset"]),dp,db,c["deadline_p"],c["deadline_b"],c["margin"])
def screen(c,method):
 if method=="nominal":return evaluate(c,1.,1.,0.,0.)
 if method=="common_endpoints":
  return all(evaluate(c,g,g,c["delay_hi"],c["delay_hi"]) for g in (c["g_lo"],1.))
 if method=="rectangle":
  return frequency_ok(c) and rectangular_certificate(*params(c),
   (c["g_lo"],1.),(c["g_lo"],1.),(0.,c["delay_hi"]),(0.,c["delay_hi"]),
   c["deadline_p"],c["deadline_b"],c["margin"],c["reset"])
 if method=="time_domain_grid":
  return all(evaluate(c,gp,gb,dp,db)
   for gp in (c["g_lo"],(1+c["g_lo"])/2,1.)
   for gb in (c["g_lo"],(1+c["g_lo"])/2,1.)
   for dp in (0.,c["delay_hi"])
   for db in (0.,c["delay_hi"]))
 raise ValueError(method)

def cases(n=90,seed=1717):
 rng=random.Random(seed);out=[]
 for i in range(n):
  reset=("full","hold","linear")[i%3]
  gap=rng.uniform(.1,.65);p1=rng.uniform(1.4,3.2);b1=rng.uniform(1.1,3.0)
  p=[Segment(0.,.4,p1),Segment(.4,.8,rng.uniform(.0,.7)),
     Segment(.8,8.,p1)]
  b=[Segment(0.,.4,b1),Segment(.4,.8,rng.uniform(.0,.7)),
     Segment(.8,8.,b1)]
  out.append({"id":i,"reset":reset,"primary":p,"backup":b,
   "pp":rng.uniform(.35,.85),"pb":rng.uniform(.35,.85),
   "tp":rng.uniform(.02,.11),"tb":rng.uniform(.05,.28),
   "g_lo":rng.uniform(.52,.83),"delay_hi":rng.uniform(.01,.16),
   "deadline_p":rng.uniform(.9,4.),"deadline_b":rng.uniform(2.,7.),
   "margin":rng.uniform(.05,.55),"f0_hz":50.,
   "df_hz":rng.uniform(.05,1.0),"floor_hz":rng.choice((49.,49.2,49.5))})
 return out

def confusion(pred,truth):
 tp=sum(p and t for p,t in zip(pred,truth))
 fp=sum(p and not t for p,t in zip(pred,truth))
 fn=sum(not p and t for p,t in zip(pred,truth))
 tn=len(pred)-tp-fp-fn
 return {"true_approvals":tp,"false_approvals":fp,
  "conservative_rejections":fn,"true_rejections":tn,
  "approval_count":tp+fp,"approval_fraction":(tp+fp)/len(pred)}

def run(n=90,seed=1717):
 data=cases(n,seed)
 methods=("nominal","common_endpoints","rectangle","time_domain_grid")
 start=time.perf_counter();pred={};cost={}
 for m in methods:
  t=time.perf_counter()
  pred[m]=[screen(c,m) for c in data]
  cost[m]=time.perf_counter()-t
 truth=pred["rectangle"] # Proven continuum iff only under independent rectangular model.
 results={m:{**confusion(pred[m],truth),"elapsed_s":cost[m]} for m in methods}
 # Correlated diagonal grid is a finite-scenario reference, NOT continuum truth.
 diag=[all(evaluate(c,g,g,dp,db) for g in (c["g_lo"],(c["g_lo"]+1)/2,1.)
  for dp in (0.,c["delay_hi"]) for db in (0.,c["delay_hi"])) for c in data]
 correlated={m:confusion(pred[m],diag) for m in methods}
 witness=correlated_counterexample()
 assert [x["passes_margin_0_4"] for x in witness["samples"]]==[True,False,True]
 assert pred["rectangle"]==pred["time_domain_grid"]
 assert all(not pred["rectangle"][i] or pred["common_endpoints"][i] for i in range(n))
 return {"benchmark":"synthetic shared scenarios; no field measurements",
  "seed":seed,"n":n,"reset_counts":{r:sum(c["reset"]==r for c in data)
    for r in ("full","hold","linear")},
  "uncertainty":"independent rectangle gamma_p,gamma_b in [g_lo,1]; breaker delays independent [0,delay_hi]",
  "frequency":"stipulated f0-df>=floor in Hz",
  "rectangular_continuum_reference":results,
  "correlated_diagonal_finite_grid_reference":correlated,
  "correlated_interior_counterexample":witness,
  "time_domain_grid_not_continuum_proof":True,
  "physical_restoration_certificates":0,
  "runtime_note":"wall-clock measurements depend on CI runner and include Python overhead"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);p.add_argument("--n",type=int,default=90)
 a=p.parse_args();d=run(a.n)
 path=pathlib.Path(a.output).resolve();path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"n":d["n"],"reference":d["rectangular_continuum_reference"],
  "correlated":d["correlated_diagonal_finite_grid_reference"]}))
