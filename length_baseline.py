"""
Length-only baseline — Acceptance Criterion 4.

Predicts a label from nothing but post length (word count). No model, no
text understanding. If your trained model can't beat this by 0.10 macro F1
on all three seeds, it hasn't learned to read the posts — just their length.

Usage:
    python length_baseline.py
    python length_baseline.py --trained results_three_seeds_before.json
    python length_baseline.py --csv labels.csv --out length_baseline_results.json
"""

import argparse
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

LABELS = ["analysis", "prescription", "motivation", "other"]
SEEDS = [42, 7, 2024]
N_BUCKETS = 4


def split_dataset(df, seed, test_size=0.15, val_size=0.15):
    """Same stratified 70/15/15 split your notebook uses, so the test rows match."""
    def _stratify_on(frame):
        counts = frame["label"].value_counts()
        return frame["label"] if counts.min() >= 2 else None

    train_val, test = train_test_split(
        df, test_size=test_size, random_state=seed, stratify=_stratify_on(df)
    )
    val_fraction = val_size / (1 - test_size)
    train, val = train_test_split(
        train_val, test_size=val_fraction, random_state=seed, stratify=_stratify_on(train_val)
    )
    return train, val, test


def word_count(text):
    return len(str(text).split())


def fit_length_baseline(train_df, n_buckets=N_BUCKETS):
    """
    Bucket posts by word count (quantile bins learned on TRAIN only), then
    assign each bucket the majority label seen in train. Returns a predict
    function closed over the learned bin edges + bucket->label map.
    """
    lengths = train_df["text"].map(word_count)

    try:
        _, bin_edges = pd.qcut(lengths, q=n_buckets, retbins=True, duplicates="drop")
    except ValueError:
        bin_edges = np.array([lengths.min(), lengths.max()])

    bin_edges = bin_edges.copy()
    bin_edges[0] = -np.inf
    bin_edges[-1] = np.inf

    bucket_ids = pd.cut(lengths, bins=bin_edges, labels=False, include_lowest=True)

    bucket_majority = {}
    for b in sorted(bucket_ids.dropna().unique()):
        posts_in_bucket = train_df.loc[bucket_ids == b, "label"]
        bucket_majority[int(b)] = posts_in_bucket.value_counts().idxmax()

    overall_majority = train_df["label"].value_counts().idxmax()

    def predict(texts):
        lens = texts.map(word_count)
        buckets = pd.cut(lens, bins=bin_edges, labels=False, include_lowest=True)
        return buckets.map(lambda b: bucket_majority.get(int(b), overall_majority) if pd.notna(b) else overall_majority)

    return predict, bin_edges, bucket_majority


def run(csv_path, out_path, trained_path):
    df = pd.read_csv(csv_path)
    if "text" not in df.columns or "label" not in df.columns:
        raise SystemExit(f"{csv_path} needs 'text' and 'label' columns. Found: {list(df.columns)}")

    all_results = []
    for seed in SEEDS:
        train, val, test = split_dataset(df, seed)
        predict, bin_edges, bucket_majority = fit_length_baseline(train)

        preds = predict(test["text"])
        gold = test["label"]

        f1_macro = f1_score(gold, preds, labels=LABELS, average="macro", zero_division=0)
        acc = accuracy_score(gold, preds)
        per_label_f1 = f1_score(gold, preds, labels=LABELS, average=None, zero_division=0)

        result = {
            "seed": seed,
            "n_test": int(len(test)),
            "accuracy": float(acc),
            "f1_macro": float(f1_macro),
            "per_label": {lab: float(f1) for lab, f1 in zip(LABELS, per_label_f1)},
        }
        all_results.append(result)
        print(f"seed {seed:>5}   accuracy {acc:.3f}   macro F1 {f1_macro:.3f}")

    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nWrote {out_path}. Commit it.")

    if trained_path:
        with open(trained_path) as f:
            trained_results = json.load(f)
        trained_by_seed = {r["seed"]: r for r in trained_results}

        print("\n| Seed | Baseline macro F1 | Trained macro F1 | Difference | Beats by ≥0.10? |")
        print("|---|---|---|---|---|")
        all_pass = True
        for r in all_results:
            t = trained_by_seed.get(r["seed"])
            if not t:
                continue
            diff = t["f1_macro"] - r["f1_macro"]
            passed = diff >= 0.10
            all_pass = all_pass and passed
            print(f"| {r['seed']} | {r['f1_macro']:.3f} | {t['f1_macro']:.3f} | {diff:+.3f} | {'yes' if passed else 'no'} |")

        print(f"\nCriterion 4 verdict: {'MET' if all_pass else 'MISSED'} (must hold on all three seeds)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="labels.csv")
    parser.add_argument("--out", default="length_baseline_results.json")
    parser.add_argument("--trained", default="results_three_seeds_before.json")
    args = parser.parse_args()
    run(args.csv, args.out, args.trained)