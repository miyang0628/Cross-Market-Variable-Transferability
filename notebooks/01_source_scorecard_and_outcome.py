"""
01_source_scorecard_and_outcome.py
CMVTS extension — build the source behavioural distribution and the realized-
divergence outcome.

Layout (run from notebooks/):
  data/     raw Findex microdata + Korean CB snapshots
  results/  derived CSVs
  results/tables/, results/figures/  outputs

Outcome = realized behavioural divergence: JSD between the Korean source card-
activity distribution and each target market's Findex card-activity distribution.
Source distribution comes from Korean CB records (NOT the survey), because the
survey records Korea's card variables as missing; using the survey as the source
inverts the sign (documented in the paper).
"""
import os, numpy as np, pandas as pd

ROOT=".."; DATA=os.path.join(ROOT,"data"); RES=os.path.join(ROOT,"results")
TAB=os.path.join(RES,"tables"); os.makedirs(TAB,exist_ok=True)
FINDEX=os.path.join(DATA,"findex_microdata_2025_labelled_update112425.csv")
CB_2022=os.path.join(DATA,"202212_개인CB.csv")   # source snapshot
YES=1
SOURCE="Korea, Rep."
ORDER=["Korea, Rep.","Indonesia","Thailand","Viet Nam","Philippines",
       "Bangladesh","Cambodia","Nepal","Pakistan","Lao PDR"]
TARGETS=[e for e in ORDER if e!=SOURCE]
CB_PRIMARY_SPEND="C1M2B4W03"; SENT=[8888888.8,-9,-99999999]

def jsd(p,q,eps=1e-12):
    p=np.asarray(p,float)+eps;q=np.asarray(q,float)+eps;p/=p.sum();q/=q.sum();m=.5*(p+q)
    kl=lambda a,b:np.sum(a*np.log2(a/b));return .5*kl(p,m)+.5*kl(q,m)
def wshare(g,v): w=g["wgt"]; return w[g[v]==YES].sum()/w.sum()

# source active share from CB
cb=pd.read_csv(CB_2022, low_memory=False)
spend=cb[CB_PRIMARY_SPEND].replace(SENT,np.nan).fillna(0).astype(float)
p_active_src=float((spend>0).mean())
src=np.array([1-p_active_src, p_active_src])
print("Korea active share (CB):", round(p_active_src,3))

# target divergence from Findex fin8 (card use)
fx=pd.read_csv(FINDEX, low_memory=False)
rows=[]
for e in TARGETS:
    g=fx[fx.economy==e]; pa=wshare(g,"fin8")
    rows.append({"economy":e,"target_active":round(pa,4),
                 "Y_realized_JSD":round(jsd(src,np.array([1-pa,pa])),4)})
out=pd.DataFrame(rows).set_index("economy")
out.to_csv(os.path.join(TAB,"outcome_realized_divergence.csv"))
print(out.to_string())
print("saved results/tables/outcome_realized_divergence.csv")
