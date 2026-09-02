# 🎙️ SpeechTranscriptEval

> **Speech Transcription and Performance Evaluation under Varying Speaking Conditions**

SpeechTranscriptEval is a research/coursework project that converts speech from audio/video recordings into text using a Speech-to-Text (ASR) model, and then rigorously evaluates transcription quality against reference (ground-truth) transcripts. The project specifically studies how **speaking conditions** — formal vs. informal speech, clear audio vs. background noise, interview-style vs. conversational — affect transcription accuracy.

---

## 📌 Project Overview

Automatic Speech Recognition (ASR) systems are widely used to transcribe interviews, lectures, meetings, and everyday conversation. However, transcription accuracy is not uniform — it varies significantly with speaking style, audio quality, accent, and background noise. This project builds a small end-to-end pipeline to:

1. Select audio/video samples representing different speaking conditions.
2. Generate transcripts with an ASR model (Whisper / Faster-Whisper).
3. Prepare reference (ground-truth) transcripts for each sample.
4. Compute objective evaluation metrics (WER, CER, BLEU, ROUGE, METEOR).
5. Compare and analyze results to identify which factors most affect accuracy.

### End-to-End Pipeline

```
┌───────────────────────────────────────────────────────────┐
│      AUDIO / VIDEO SAMPLES (different speaking conditions) │
└───────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Audio Extraction /   │
                     │      Preprocessing     │
                     │   (16 kHz, mono WAV)   │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Speech-to-Text ASR   │
                     │ (Whisper/Faster-Whisper)│
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  Generated Transcript  │
                     └───────────┬───────────┘
                                 │
                     ┌───────────┴───────────┐
                     ▼                       ▼
           Reference Transcript      Normalization
                     │                       │
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │  Evaluation Metrics    │
                     │  WER · CER · BLEU      │
                     │  ROUGE · METEOR        │
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │ Comparative Analysis   │
                     │ (by speaking condition)│
                     └───────────────────────┘
```

---

## 🧪 Case Study Design

Samples are grouped into **paired conditions** so that the *only* meaningfully varying factor between each pair is the one being studied:

| Category | Condition A | Condition B | Factor Studied |
|---|---|---|---|
| Speaking style | Formal speech (e.g. news broadcast, prepared talk) | Informal conversation (casual dialogue) | Register / spontaneity, filler words |
| Audio quality | Clear studio-quality speech | Speech with background noise (traffic, crowd, music) | Signal-to-noise ratio |
| Interaction type | One-on-one interview | Multi-speaker conversation / panel | Overlapping speech, speaker changes |
| Accent/pace | Standard-paced, neutral-accent speech | Fast speech or strong regional accent | Pronunciation variability |

Each sample is stored in `data/samples/` with a matching hand-verified reference transcript in `data/reference_transcripts/`. See [`data/README.md`](data/README.md) for the naming convention and [`docs/case_study.md`](docs/case_study.md) for the full methodology.

---

## 📊 Evaluation Metrics

| Metric | Level | What it captures |
|---|---|---|
| **WER** (Word Error Rate) | Word | Substitutions, deletions, insertions relative to reference word count |
| **CER** (Character Error Rate) | Character | Fine-grained errors, useful for short/technical utterances |
| **BLEU** | N-gram | Precision-oriented overlap, borrowed from MT evaluation |
| **ROUGE** | N-gram / longest common subsequence | Recall-oriented overlap |
| **METEOR** | Word (with stemming/synonym matching) | More linguistically aware alignment than BLEU |

Lower WER/CER and higher BLEU/ROUGE/METEOR indicate a more accurate transcript. See [`docs/evaluation_metrics.md`](docs/evaluation_metrics.md) for formulas and interpretation notes.

---

## 📁 Project Structure

```
SpeechTranscriptEval/
│
├── app.py                     # Streamlit interface for the full workflow
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md              # Dataset & naming convention
│   ├── samples/                # Raw audio/video samples (not committed - see .gitignore)
│   ├── reference_transcripts/  # Ground-truth .txt transcripts
│   └── results/                # Generated transcripts + metrics CSV output
│
├── docs/
│   ├── case_study.md           # Full methodology & sample selection rationale
│   └── evaluation_metrics.md   # Metric formulas & interpretation guide
│
├── scripts/
│   └── run_evaluation.py       # CLI batch runner: transcribe + evaluate all samples
│
└── src/
    ├── __init__.py
    ├── audio_processor.py      # Load, convert, and standardize audio
    ├── transcriber.py          # ASR wrapper (Whisper / Faster-Whisper)
    ├── metrics.py              # WER, CER, BLEU, ROUGE, METEOR computation
    └── report_generator.py     # Aggregate results into comparison tables/plots
```

---

## ⚙️ Requirements

- Python 3.10+
- FFmpeg (for audio/video extraction)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Add your samples

Place audio/video files in `data/samples/` and their matching ground-truth transcripts (plain `.txt`) in `data/reference_transcripts/` using the same base filename. See [`data/README.md`](data/README.md).

### 2. Run the Streamlit app

```bash
streamlit run app.py
```

Upload a sample, generate a transcript, paste/upload the reference, and view WER/CER/BLEU/ROUGE/METEOR instantly.

### 3. Batch-evaluate the whole dataset from the command line

```bash
python scripts/run_evaluation.py --samples-dir data/samples --refs-dir data/reference_transcripts --out data/results/evaluation_results.csv
```

This transcribes every sample, scores it against its reference, and writes a single CSV with one row per sample plus its speaking-condition label — ready for the comparative analysis.

---

## 📈 Analysis & Findings

After running the batch evaluation, results are aggregated by condition (formal vs. informal, clean vs. noisy, etc.) so trends can be compared directly — e.g. average WER for noisy audio vs. clean audio. Findings and discussion for this specific study go in [`docs/case_study.md`](docs/case_study.md) under "Results & Analysis," and the raw per-sample scores live in `data/results/evaluation_results.csv`.

---

## 🎯 Expected Outcome

A comparative analysis demonstrating how factors such as **speaking style, background noise, speaker interaction, accent, and pace** influence transcription accuracy — quantified through WER, CER, BLEU, ROUGE, and METEOR, and discussed in terms of practical implications for ASR deployment (e.g. captioning, meeting transcription, voice assistants).

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Interactive UI |
| OpenAI Whisper / Faster-Whisper | Speech-to-text transcription |
| FFmpeg | Audio/video extraction & conversion |
| jiwer | WER / CER computation |
| sacrebleu | BLEU computation |
| rouge-score | ROUGE computation |
| NLTK | METEOR computation |
| Pandas / Matplotlib | Results aggregation & visualization |

---

## 📄 License

No license file is currently included. Add a `LICENSE` file (e.g. MIT) before making the repository public if you intend others to reuse the code.

---

## 👤 Author

Coursework project — Speech Transcription and Performance Evaluation.
