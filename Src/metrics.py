"""
metrics.py

Computes transcription-quality metrics: WER, CER, BLEU, ROUGE, METEOR.
"""

import re
import string


def normalize_text(text: str) -> str:
    """Lowercase, strip punctuation, and collapse whitespace.

    Keeping normalization consistent between hypothesis and reference is
    essential for fair comparison.
    """
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_wer(reference: str, hypothesis: str) -> float:
    """Word Error Rate using jiwer. Returned as a percentage (0-100+)."""
    import jiwer
    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)
    if not ref:
        return 0.0 if not hyp else 100.0
    return jiwer.wer(ref, hyp) * 100


def compute_cer(reference: str, hypothesis: str) -> float:
    """Character Error Rate using jiwer. Returned as a percentage (0-100+)."""
    import jiwer
    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)
    if not ref:
        return 0.0 if not hyp else 100.0
    return jiwer.cer(ref, hyp) * 100


def compute_bleu(reference: str, hypothesis: str) -> float:
    """Corpus BLEU using sacrebleu. Returned 0-100."""
    import sacrebleu
    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)
    if not ref or not hyp:
        return 0.0
    result = sacrebleu.sentence_bleu(hyp, [ref])
    return result.score


def compute_rouge(reference: str, hypothesis: str) -> dict:
    """ROUGE-1 / ROUGE-2 / ROUGE-L F-measure using rouge-score. Returned 0-1."""
    from rouge_score import rouge_scorer
    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    if not ref or not hyp:
        return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
    scores = scorer.score(ref, hyp)
    return {k: v.fmeasure for k, v in scores.items()}


def compute_meteor(reference: str, hypothesis: str) -> float:
    """METEOR score using NLTK. Returned 0-1."""
    import nltk
    for resource in ("wordnet", "omw-1.4", "punkt", "punkt_tab"):
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass

    from nltk.translate.meteor_score import meteor_score
    from nltk.tokenize import word_tokenize

    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)
    if not ref or not hyp:
        return 0.0

    ref_tokens = word_tokenize(ref)
    hyp_tokens = word_tokenize(hyp)
    return meteor_score([ref_tokens], hyp_tokens)


def evaluate_transcription(reference: str, hypothesis: str) -> dict:
    """Run all metrics and return a single results dict.

    Args:
        reference: Ground-truth transcript text.
        hypothesis: ASR-generated transcript text.
    """
    rouge = compute_rouge(reference, hypothesis)

    return {
        "wer": round(compute_wer(reference, hypothesis), 2),
        "cer": round(compute_cer(reference, hypothesis), 2),
        "bleu": round(compute_bleu(reference, hypothesis), 2),
        "rouge1": round(rouge["rouge1"], 4),
        "rouge2": round(rouge["rouge2"], 4),
        "rougeL": round(rouge["rougeL"], 4),
        "meteor": round(compute_meteor(reference, hypothesis), 4),
    }
