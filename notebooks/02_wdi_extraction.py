"""
02_wdi_extraction.py
Extract open macro indicators from the World Bank WDI API (no key needed).
Predictor = infrastructure + macro-scale ONLY (WDI-only, disjoint from the
Findex-derived outcome). Saves results/wdi_macro_latest.csv and wdi_macro_2021.csv.
Run locally with network access to api.worldbank.org.
"""
import os, json, time, urllib.request, pandas as pd
ROOT=".."; RES=os.path.join(ROOT,"results"); os.makedirs(RES,exist_ok=True)
COUNTRIES={"KOR":"Korea, Rep.","IDN":"Indonesia","THA":"Thailand","VNM":"Viet Nam",
           "PHL":"Philippines","BGD":"Bangladesh","KHM":"Cambodia","NPL":"Nepal",
           "PAK":"Pakistan","LAO":"Lao PDR"}
# WDI-only predictor indicators (infrastructure + macro scale)
IND={"IT.NET.USER.ZS":"A1_internet_use_pct","IT.CEL.SETS.P2":"A2_mobile_subs_p100",
     "IT.NET.BBND.P2":"A3_fixed_bbnd_p100","IT.NET.SECR.P6":"A6_secure_servers_p1m",
     "NY.GNP.PCAP.CD":"D1_gni_pc_atlas","SP.URB.TOTL.IN.ZS":"D2_urban_pct",
     "SL.TLF.CACT.ZS":"D3_labor_participation_pct","FS.AST.PRVT.GD.ZS":"D4_domestic_credit_priv_gdp"}
API="https://api.worldbank.org/v2/country/{iso}/indicator/{code}?format=json&date=2021:2024&per_page=100"
def fetch(iso,code):
    try:
        with urllib.request.urlopen(API.format(iso=iso,code=code),timeout=30) as r: d=json.load(r)
        return [{"iso":iso,"code":code,"year":int(x["date"]),"value":x["value"]}
                for x in (d[1] or []) if x["value"] is not None]
    except Exception as e:
        print("warn",iso,code,type(e).__name__); return []
rec=[]
for iso in COUNTRIES:
    for code in IND: rec.extend(fetch(iso,code))
    time.sleep(0.3)
raw=pd.DataFrame(rec)
def pick(g,y):
    v=g.loc[g.year==y,"value"]
    if len(v): return v.iloc[0]
    le=g[g.year<=2024].sort_values("year"); return le["value"].iloc[-1] if len(le) else None
for yr,tag in [(2021,"2021"),(2024,"latest")]:
    rows=[]
    for (iso,code),g in raw.groupby(["iso","code"]):
        rows.append({"economy":COUNTRIES[iso],"indicator":IND[code],"value":pick(g,yr)})
    wide=pd.DataFrame(rows).pivot(index="economy",columns="indicator",values="value").reindex(list(COUNTRIES.values()))
    wide.to_csv(os.path.join(RES,f"wdi_macro_{tag}.csv"))
    print(f"saved results/wdi_macro_{tag}.csv")
