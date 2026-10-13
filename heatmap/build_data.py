#!/usr/bin/env python3
"""Build the data behind the /prism/data page from the PRISM repository.

    python heatmap/build_data.py --prism <path to a clone of github.com/gomesgroup/PRISM>

Reads
    <prism>/3_ml_model/data/datasheets/PRISM_rates.xlsx               rate constants (1.5x control)
    <prism>/3_ml_model/data/datasheets/PRISM_rates_unmeasurable.xlsx  classes and notes of the rest
    <prism>/3_ml_model/data/datasheets/PRISM_substrate_scope.xlsx     SMILES
    <prism>/2_rate_fitting/outputs/well_level_kept_excluded.csv       per-well half-lives

Writes, in heatmap/data/
    rate_constants.csv   k (M^-1 min^-1) for every acyl chloride x amine pair; blank if not measurable
    reaction_classes.csv measurable / instant / un-reactive / undetermined for every pair
    rate_plots.json      per pair: 1/[A]0 against t1/2 for each well, whether it was fitted,
                         the no-amine control, the fitted line, the class and its note
    acids_smiles.csv, amines_smiles.csv
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CLASS_NAME = {"measurable": "measurable", "instant": "instant",
              "slow": "un-reactive", "undetermined": "undetermined"}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prism", type=Path, required=True)
    p.add_argument("--margin", default="1p5x")
    p.add_argument("--out", type=Path, default=HERE / "data")
    a = p.parse_args()
    sheets = a.prism / "3_ml_model" / "data" / "datasheets"
    rates = pd.read_excel(sheets / "PRISM_rates.xlsx")
    unmeas = pd.read_excel(sheets / "PRISM_rates_unmeasurable.xlsx")
    scope = pd.read_excel(sheets / "PRISM_substrate_scope.xlsx", sheet_name=None)
    wells = pd.read_csv(a.prism / "2_rate_fitting" / "outputs" / "well_level_kept_excluded.csv")
    status = "status_" + a.margin

    rates = rates.assign(rate_class="measurable", note="")
    table = pd.concat([rates, unmeas], ignore_index=True)
    table["name_acyl"] = table.acyl_chloride.astype(str).str.replace(r"-\d[A-C]$", "", regex=True)
    acyl_name = table.groupby("acyl_label").name_acyl.first().sort_index()
    amine_name = table.groupby("amine_label").amine.first().sort_index()

    k = pd.DataFrame(np.nan, index=acyl_name.values, columns=amine_name.values)
    cls = pd.DataFrame("", index=acyl_name.values, columns=amine_name.values)
    plots = {}
    for _, r in table.iterrows():
        acyl, amine = acyl_name[r.acyl_label], amine_name[r.amine_label]
        c = CLASS_NAME[r.rate_class]
        cls.loc[acyl, amine] = c
        if c == "measurable":
            k.loc[acyl, amine] = r.k_corrected
        # plates of this pair (several for the 4-fluorobenzoyl chloride batches)
        plates = [s.strip() for s in str(r.batch).split(",")] if isinstance(r.batch, str) else [None]
        plate_names = [acyl if b is None else f"{acyl}-{b}" for b in plates]
        w = wells[wells.acyl_chloride.isin(plate_names) & (wells.amine == r.amine)]
        best, best_n = None, -1
        for name, g in w.groupby("acyl_chloride"):
            n = int((g[status] == "kept").sum())
            if n > best_n:
                best, best_n = name, n
        g = w[w.acyl_chloride == best].sort_values("conc_mM", ascending=False)
        pts = g[g.amine_time_min.notna() & g.stored_ordinate_2_over_A0.notna()]
        ctl = g[g.control_time_min.notna() & g.stored_ordinate_2_over_A0.notna()]
        used = pts[pts[status] == "kept"]
        fit = None
        if len(used) >= 2 and used.amine_time_min.nunique() > 1:
            slope, icpt = np.polyfit(used.amine_time_min, used.stored_ordinate_2_over_A0 / 2, 1)
            fit = {"slope": float(slope), "intercept": float(icpt)}
        plots[f"{acyl}||{amine}"] = {
            "acid_chloride": acyl, "amine": amine, "reaction": r.reaction,
            "rate_class": c, "k": None if c != "measurable" else float(r.k_corrected),
            "n_batches": len(plates) if plates != [None] else 1,
            "plate": best, "note": str(r.note) if isinstance(r.note, str) else "",
            "t_half": pts.amine_time_min.tolist(),
            "inv_A0": (pts.stored_ordinate_2_over_A0 / 2).tolist(),
            "used": (pts[status] == "kept").tolist(),
            "control_t_half": ctl.control_time_min.tolist(),
            "control_inv_A0": (ctl.stored_ordinate_2_over_A0 / 2).tolist(),
            "fit": fit}

    a.out.mkdir(parents=True, exist_ok=True)
    k.to_csv(a.out / "rate_constants.csv")
    cls.to_csv(a.out / "reaction_classes.csv")
    with open(a.out / "rate_plots.json", "w") as f:
        json.dump(plots, f, separators=(",", ":"))

    acy = scope["acyls"].dropna(subset=["smiles"]).drop_duplicates("acyl_label").set_index("acyl_label").smiles
    ami = scope["amine"].drop_duplicates("amine_label").set_index("amine_label").smiles
    pd.DataFrame({"index": acyl_name.values, "acid_smiles": acy.reindex(acyl_name.index).values}).to_csv(
        a.out / "acids_smiles.csv", index=False)
    pd.DataFrame({"index": amine_name.values, "amine_smiles": ami.reindex(amine_name.index).values}).to_csv(
        a.out / "amines_smiles.csv", index=False)
    print(f"{k.shape[0]} acyl chlorides x {k.shape[1]} amines; classes "
          f"{pd.Series(cls.values.ravel()).value_counts().to_dict()}; rate plots {len(plots)} -> {a.out}")


if __name__ == "__main__":
    main()
