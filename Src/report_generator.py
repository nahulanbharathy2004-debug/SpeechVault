"""
report_generator.py

Aggregates per-sample evaluation results into comparison tables,
grouped by speaking-condition label parsed from the filename.
"""

import pandas as pd


def infer_condition(sample_name: str) -> str:
    """Infer the speaking-condition label from a filename prefix.

    Expects names like 'formal_newsanchor_01', 'noisy_interview_02', etc.
    (see data/README.md for the naming convention). Falls back to
    'unknown' if no recognized label prefix is found.
    """
    known_labels = ["formal", "informal", "clean", "noisy", "interview", "multispeaker"]
    lower = sample_name.lower()
    matches = [label for label in known_labels if lower.startswith(label)]
    return matches[0] if matches else "unknown"


def build_results_table(rows: list[dict]) -> pd.DataFrame:
    """Build a DataFrame from a list of per-sample result dicts.

    Each row dict is expected to have at least:
        sample, condition, wer, cer, bleu, rouge1, rouge2, rougeL, meteor
    """
    df = pd.DataFrame(rows)
    if "condition" not in df.columns and "sample" in df.columns:
        df["condition"] = df["sample"].apply(infer_condition)
    return df


def summarize_by_condition(df: pd.DataFrame) -> pd.DataFrame:
    """Average each metric within each speaking-condition group."""
    metric_cols = [c for c in ["wer", "cer", "bleu", "rouge1", "rouge2", "rougeL", "meteor"]
                   if c in df.columns]
    return df.groupby("condition")[metric_cols].mean().round(3).reset_index()


def save_results(df: pd.DataFrame, out_path: str) -> None:
    df.to_csv(out_path, index=False)
