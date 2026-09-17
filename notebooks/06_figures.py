"""
06_figures.py
Regenerate all data figures (greyscale, 600 dpi, PNG+PDF) from the result tables.
Reads results/tables/*.csv, writes results/figures/*.{png,pdf}.
"""
import os, numpy as np, pandas as pd
from scipy import stats
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
ROOT=".."; TAB=os.path.join(ROOT,"results","tables"); FIG=os.path.join(ROOT,"results","figures")
os.makedirs(FIG,exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size":11,"axes.edgecolor":"0.2","axes.linewidth":0.8,"grid.color":"0.85"})
def save(fig,name):
    for ext in ("png","pdf"): fig.savefig(f"{FIG}/{name}.{ext}",dpi=600,bbox_inches="tight")
    plt.close(fig)

comp=pd.read_csv(os.path.join(TAB,"cmvts_components.csv"),index_col=0)
Y=pd.read_csv(os.path.join(TAB,"outcome_realized_divergence.csv"),index_col=0)["Y_realized_JSD"]
grid=pd.read_csv(os.path.join(TAB,"two_dimensional_grid.csv"),index_col=0)
df=comp.join(Y)

# fig_5_2 predictor-outcome
x,y=df["macroCMVTS"],df["Y_realized_JSD"]
fig,ax=plt.subplots(figsize=(6.4,5.2))
ax.scatter(x,y,s=90,c="0.35",edgecolors="black",linewidths=0.8,zorder=3)
b,a=np.polyfit(x,y,1);xs=np.linspace(x.min(),x.max(),50);ax.plot(xs,a+b*xs,color="0.1",lw=1.3)
for c in df.index: ax.annotate(c,(x[c],y[c]),xytext=(4,4),textcoords="offset points",fontsize=8.5)
rs,ps=stats.spearmanr(x,y)
ax.text(0.03,0.04,f"Spearman = {rs:+.2f} (p={ps:.3f})",transform=ax.transAxes,fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4",fc="white",ec="0.5"))
ax.set_xlabel("Transferability (macro-CMVTS, WDI-only)");ax.set_ylabel("Realized divergence (JSD)")
fig.tight_layout();save(fig,"fig_5_2_predictor_outcome")

# fig_2d grid
GREY={"Q1":"0.15","Q2":"0.45","Q3":"0.65","Q4":"0.85"};MK={"Q1":"o","Q2":"s","Q3":"^","Q4":"D"}
fig,ax=plt.subplots(figsize=(6.6,5.6))
for q in ["Q1","Q2","Q3","Q4"]:
    m=grid["quadrant"]==q
    ax.scatter(grid.loc[m,"transferability"],grid.loc[m,"absorptive_FIE"],s=95,c=GREY[q],
               marker=MK[q],edgecolors="black",linewidths=0.8,label=q,zorder=3)
ax.axvline(grid["transferability"].median(),color="0.3",ls="--");ax.axhline(grid["absorptive_FIE"].median(),color="0.3",ls="--")
for c in grid.index: ax.annotate(c,(grid.loc[c,"transferability"],grid.loc[c,"absorptive_FIE"]),
                                 xytext=(4,4),textcoords="offset points",fontsize=8.5)
ax.set_xlabel("Transferability (macro-CMVTS, WDI-only)");ax.set_ylabel("Absorptive capacity (FIE)")
ax.legend(loc="upper center",bbox_to_anchor=(0.5,-0.12),ncol=4,frameon=False)
fig.tight_layout();save(fig,"fig_2d_decision_grid")
print("figures written to results/figures/")
