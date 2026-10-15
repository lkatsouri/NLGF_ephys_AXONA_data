import pandas as pd

src = "/Users/loukia/Library/CloudStorage/Dropbox-UCL/Loukia Katsouri/DataProtocolsEquipment/Ephys_Analysis/RobinData/individual_examples/theta_plv_summary.xlsx"
out = src.replace("theta_plv_summary.xlsx", "theta_plv_deciles.xlsx")

df = pd.read_excel(src)

def assign_deciles(s):
    # rank 1 = highest PLV; 'first' breaks ties so every decile is filled
    ranks = s.rank(method="first", ascending=False)
    return pd.qcut(ranks, 10, labels=range(1, 11)).astype(int)  # 1 = top 10%

# deciles computed within each genotype x environment
df["decile"] = df.groupby(["genotype", "environment"])["phase_locked_value"].transform(assign_deciles)
df = df.sort_values(["genotype", "environment", "decile", "phase_locked_value"],
                    ascending=[False, True, True, False])

summary = (df.groupby(["genotype", "environment", "decile"])["phase_locked_value"]
             .agg(n="count", min="min", max="max", mean="mean").reset_index())

with pd.ExcelWriter(out) as xw:
    df.to_excel(xw, sheet_name="cells_with_decile", index=False)
    summary.to_excel(xw, sheet_name="decile_summary", index=False)
print(out)
print(summary.head(12))
