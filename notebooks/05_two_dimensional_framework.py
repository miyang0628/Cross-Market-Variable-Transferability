"""
05_two_dimensional_framework.py
Two-dimensional decision framework: transferability (macro-CMVTS, WDI-only) x
absorptive capacity (IMF FIE sub-index). Checks FIE independence, assigns quadrants,
tests placement stability under jitter. Saves results/tables/two_dimensional_grid.csv.
"""
import os, numpy as np, pandas as pd
from scipy import stats
ROOT=".."; RES=os.path.join(ROOT,"results"); TAB=os.path.join(RES,"tables")
comp=pd.read_csv(os.path.join(TAB,"cmvts_components.csv"),index_col=0)
lab=pd.read_csv(os.path.join(TAB,"imf_fdi_label.csv"),index_col=0)  # move imf_fdi_label here
TARGETS=list(comp.index)
mc=comp["macroCMVTS"]; FIE=lab["FIE"].reindex(TARGETS)
rs,ps=stats.spearmanr(mc,FIE)
print(f"FIE independence: Spearman {rs:+.3f} (p={ps:.3f})  (near 0 => two axes independent)")
tmed,amed=mc.median(),FIE.median()
def quad(t,a):
    ht,ha=t>=tmed,a>=amed
    return "Q1" if ht and ha else "Q3" if ht and not ha else "Q2" if (not ht) and ha else "Q4"
g=pd.DataFrame({"transferability":mc,"absorptive_FIE":FIE})
g["quadrant"]=[quad(g.loc[e,"transferability"],g.loc[e,"absorptive_FIE"]) for e in TARGETS]
# jitter stability
rng=np.random.default_rng(0);sT=mc.std()*.15;sA=FIE.std()*.15
base={e:g.loc[e,"quadrant"] for e in TARGETS};flips={e:0 for e in TARGETS}
for _ in range(2000):
    for e in TARGETS:
        if quad(mc[e]+rng.normal(0,sT),FIE[e]+rng.normal(0,sA))!=base[e]: flips[e]+=1
g["flip_rate"]=[flips[e]/2000 for e in TARGETS]
g.round(4).to_csv(os.path.join(TAB,"two_dimensional_grid.csv"))
print(g.round(4).sort_values(["quadrant","transferability"],ascending=[True,False]).to_string())
print("saved results/tables/two_dimensional_grid.csv")
