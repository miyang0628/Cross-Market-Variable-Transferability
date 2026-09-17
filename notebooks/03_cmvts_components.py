"""
03_cmvts_components.py
Compute the macro predictor components on the WDI-only indicator set:
  C2 = cross-country rank alignment (redefined; robust when source is extremal)
  C3 = cosine similarity (unit-max scaling, rank-preserving)
  macro-CMVTS = w2*C2 + w3*C3  (equal weight primary)
Saves results/tables/cmvts_components.csv.
"""
import os, numpy as np, pandas as pd
ROOT=".."; RES=os.path.join(ROOT,"results"); TAB=os.path.join(RES,"tables"); os.makedirs(TAB,exist_ok=True)
SOURCE="Korea, Rep."
ORDER=["Korea, Rep.","Indonesia","Thailand","Viet Nam","Philippines",
       "Bangladesh","Cambodia","Nepal","Pakistan","Lao PDR"]
TARGETS=[e for e in ORDER if e!=SOURCE]
LAO_D4=55.0
def load(path):
    m=pd.read_csv(path,index_col=0).reindex(ORDER)
    if "D4_domestic_credit_priv_gdp" in m.columns and pd.isna(m.loc["Lao PDR","D4_domestic_credit_priv_gdp"]):
        m.loc["Lao PDR","D4_domestic_credit_priv_gdp"]=LAO_D4
    return m
def C2cc(M):
    R=M.rank(ascending=False);kr=R.loc[SOURCE];n=len(ORDER);out={}
    for e in TARGETS:
        t=R.loc[e];c=kr.notna()&t.notna();out[e]=1-((kr[c]-t[c]).abs()/(n-1)).mean()
    return pd.Series(out)
def C3(M):
    m=M.copy()
    if "D1_gni_pc_atlas" in m.columns: m["D1_gni_pc_atlas"]=np.log(m["D1_gni_pc_atlas"])
    S=m/m.max();kr=S.loc[SOURCE].values;out={}
    for e in TARGETS:
        t=S.loc[e].values;c=~np.isnan(kr)&~np.isnan(t)
        out[e]=float(np.dot(kr[c],t[c])/(np.linalg.norm(kr[c])*np.linalg.norm(t[c])))
    return pd.Series(out)
M=load(os.path.join(RES,"wdi_macro_latest.csv"))
c2,c3=C2cc(M),C3(M); mc=0.5*c2+0.5*c3
df=pd.DataFrame({"C2":c2.round(4),"C3":c3.round(4),"macroCMVTS":mc.round(4)}).reindex(TARGETS)
df.to_csv(os.path.join(TAB,"cmvts_components.csv"))
print(df.to_string()); print("saved results/tables/cmvts_components.csv")
