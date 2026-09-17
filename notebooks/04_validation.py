"""
04_validation.py
Circularity-free validation + robustness:
  (a) predictor-outcome Spearman (headline)
  (b) leave-one-out
  (c) weight insensitivity
Reads cmvts_components.csv and outcome_realized_divergence.csv.
"""
import os, numpy as np, pandas as pd
from scipy import stats
ROOT=".."; TAB=os.path.join(ROOT,"results","tables")
comp=pd.read_csv(os.path.join(TAB,"cmvts_components.csv"),index_col=0)
Y=pd.read_csv(os.path.join(TAB,"outcome_realized_divergence.csv"),index_col=0)["Y_realized_JSD"]
d=comp.join(Y).dropna()
def sp(x,y):
    m=pd.DataFrame({"x":x,"y":y}).dropna();return stats.spearmanr(m["x"],m["y"])
print("(a) headline:")
for col in ["C2","C3","macroCMVTS"]:
    rs,ps=sp(d[col],d["Y_realized_JSD"]); print(f"  {col:12s} Spearman {rs:+.3f} (p={ps:.3f})")
print("\n(b) leave-one-out (macroCMVTS):")
base=d[["macroCMVTS","Y_realized_JSD"]]
for drop in base.index:
    rs=stats.spearmanr(*base.drop(drop).T.values)[0]; print(f"  drop {drop:12s} -> {rs:+.3f}")
print("\n(c) weight grid:")
for w2 in np.round(np.arange(0,1.0001,0.1),1):
    mc=w2*d["C2"]+(1-w2)*d["C3"]; rs=sp(mc,d["Y_realized_JSD"])[0]; print(f"  w2={w2}: {rs:+.3f}")
