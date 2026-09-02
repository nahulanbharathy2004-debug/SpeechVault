# 🎙️ SpeechTranscriptEval

## Speech Transcription and Performance Evaluation under Varying Speaking Conditions

**SpeechTranscriptEval** is a research and coursework project designed to convert speech from audio and video recordings into text using **Automatic Speech Recognition (ASR)** models and evaluate the quality of the generated transcripts against verified reference transcripts.

The primary objective of the project is not only to produce speech transcripts, but also to investigate how different **speaking conditions** influence transcription accuracy.

The project studies factors such as:

* Formal vs. informal speech
* Clear vs. noisy audio
* One-on-one interviews vs. multi-speaker conversations
* Standard-paced vs. fast speech
* Neutral-accent vs. regional-accent speech
* Different levels of background noise
* Different speaking styles and interaction patterns

The system provides an end-to-end workflow covering **audio preprocessing, speech recognition, transcript normalization, objective evaluation, result aggregation, visualization, and comparative analysis**.

---

# 📌 Project Overview

Automatic Speech Recognition systems are widely used for:

* Lecture transcription
* Interview transcription
* Meeting transcription
* Automatic captioning
* Voice assistants
* Video-to-text applications
* Conversational systems

However, ASR accuracy is affected by real-world conditions. A model that performs well on clean, clearly spoken audio may produce more errors when the recording contains background noise, multiple speakers, overlapping speech, strong accents, or rapid speech.

SpeechTranscriptEval is designed as an experimental platform for measuring these differences quantitatively.

### Main Objectives

The project aims to:

1. Collect representative audio/video samples.
2. Organize samples according to speaking conditions.
3. Extract and standardize speech audio.
4. Generate transcripts using ASR models.
5. Prepare hand-verified reference transcripts.
6. Normalize reference and generated text.
7. Calculate transcription evaluation metrics.
8. Compare results across speaking conditions.
9. Generate tables and visualizations.
10. Identify factors that significantly influence transcription accuracy.

---

# 🔄 End-to-End Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│              AUDIO / VIDEO SAMPLES                          │
│              Different Speaking Conditions                  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Media Detection     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Audio Extraction    │
                    │ / Conversion        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Audio Preprocessing │
                    │ 16 kHz / Mono WAV   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Speech Recognition  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │ Whisper         │         │ Faster-Whisper  │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Generated Transcript│
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       Reference Transcript          Text Normalization
                │                             │
                └──────────────┬──────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Evaluation Metrics  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
            WER               CER              BLEU
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Comparative Analysis│
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Tables / Graphs /   │
                    │ Research Findings   │
                    └─────────────────────┘
```

---

# ✨ Key Features

| Feature                  | Description                                                 |
| ------------------------ | ----------------------------------------------------------- |
| 🎙️ Audio Processing     | Load, validate, convert, and standardize speech audio       |
| 🎬 Video Processing      | Extract audio from video recordings using FFmpeg            |
| 🔊 Audio Standardization | Convert audio to 16 kHz mono WAV                            |
| 🤖 ASR Transcription     | Generate speech transcripts using Whisper or Faster-Whisper |
| ⚡ Fast Transcription     | Support efficient Faster-Whisper transcription              |
| 📊 WER Evaluation        | Calculate Word Error Rate                                   |
| 🔤 CER Evaluation        | Calculate Character Error Rate                              |
| 📈 BLEU Evaluation       | Measure n-gram similarity                                   |
| 📝 Reference Comparison  | Compare generated transcripts with ground truth             |
| 🧹 Text Normalization    | Normalize case, punctuation, and whitespace                 |
| 📋 Batch Evaluation      | Evaluate multiple samples automatically                     |
| 📊 Result Aggregation    | Group results by speaking condition                         |
| 📉 Visualization         | Generate comparison charts and performance plots            |
| 🧪 Case Study            | Compare ASR performance under controlled conditions         |
| 🖥️ Streamlit UI         | Provide an interactive browser-based workflow               |
| 💾 CSV Results           | Store per-sample evaluation results                         |

---

# 🔄 Application Workflow

## 1. Input

SpeechTranscriptEval accepts audio and video recordings representing different speaking conditions.

Supported input examples include:

* WAV audio
* MP3 audio
* M4A audio
* MP4 video
* Other FFmpeg-compatible media formats

Samples are stored in:

```text
data/samples/
```

Each sample should have a corresponding ground-truth transcript.

---

## 2. Dataset Organization

Every audio/video sample is paired with a reference transcript using the same base filename.

Example:

```text
data/samples/
├── formal_speech_01.mp4
├── informal_speech_01.mp4
├── clean_audio_01.wav
└── noisy_audio_01.wav

data/reference_transcripts/
├── formal_speech_01.txt
├── informal_speech_01.txt
├── clean_audio_01.txt
└── noisy_audio_01.txt
```

The reference transcript should be manually checked so that it represents the actual spoken content as accurately as possible.

---

## 3. Media Detection

The application determines whether the input is an audio or video file.

For video recordings, the audio track must first be extracted before speech recognition can be performed.

---

## 4. Audio Extraction

FFmpeg is used to extract speech audio from video files.

The audio is standardized to:

```text
Sample Rate : 16,000 Hz
Channels    : Mono
Format      : PCM WAV
```

Standardization provides a consistent input format for the ASR models.

---

## 5. Speech Recognition

The processed audio is passed to an ASR model.

The project supports:

```text
Audio
  │
  ├──► Whisper
  │
  └──► Faster-Whisper
```

The generated output is stored as the hypothesis transcript.

---

## 6. Reference Comparison

When a reference transcript is available, the generated transcript is compared against the ground truth.

The two texts are normalized before evaluation to reduce differences caused only by formatting.

Normalization may include:

* Converting text to lowercase
* Removing punctuation
* Normalizing whitespace
* Comparing equivalent textual representations

---

## 7. Evaluation

The normalized transcripts are evaluated using:

* Word Error Rate
* Character Error Rate
* BLEU
* ROUGE
* METEOR

These metrics provide different perspectives on transcription quality.

---

## 8. Comparative Analysis

After individual samples are evaluated, results are grouped according to their speaking condition.

For example:

```text
Clean Audio
     │
     ▼
Average WER
     │
     ▼
Compare with
     │
     ▼
Noisy Audio
     │
     ▼
Average WER
```

This allows the study to determine whether the selected condition is associated with higher or lower transcription error.

---

# 🧪 Case Study Design

The case study is organized around controlled comparisons.

The objective is to compare two conditions while keeping other factors as similar as reasonably possible.

| Category       | Condition A             | Condition B                | Factor Studied            |
| -------------- | ----------------------- | -------------------------- | ------------------------- |
| Speaking Style | Formal speech           | Informal conversation      | Register and spontaneity  |
| Audio Quality  | Clear audio             | Background-noise audio     | Signal-to-noise ratio     |
| Interaction    | One speaker/interview   | Multi-speaker conversation | Speaker changes           |
| Pace           | Standard-paced speech   | Fast speech                | Speaking rate             |
| Accent         | Neutral/standard accent | Regional/stronger accent   | Pronunciation variability |

The results from these comparisons form the basis of the research discussion.

---

# 🎤 Speaking Conditions

## Formal vs. Informal Speech

Formal speech may include prepared presentations, news broadcasts, lectures, or structured talks.

Informal speech may contain:

* Fillers
* Hesitations
* Self-corrections
* Short interruptions
* Casual expressions
* Less predictable sentence structures

The comparison investigates whether spontaneous speech results in increased transcription errors.

---

## Clear vs. Noisy Audio

Clear recordings provide relatively favorable conditions for ASR systems.

Noisy recordings may contain:

* Traffic sounds
* Crowd noise
* Music
* Environmental sounds
* Multiple background voices

The comparison measures how environmental noise influences transcription accuracy.

---

## One-on-One vs. Multi-Speaker Speech

One-on-one recordings generally have clearer speaker boundaries.

Multi-speaker recordings may introduce:

* Speaker changes
* Overlapping speech
* Interruptions
* Different speaking rates
* Different vocal characteristics

This condition evaluates how interaction complexity affects ASR performance.

---

## Standard vs. Fast Speech

Rapid speech can make individual words harder for an ASR model to identify.

The comparison examines whether increased speaking rate results in:

* More substitutions
* More deletions
* More insertions
* Higher WER
* Higher CER

---

# 🤖 Speech Recognition Models

SpeechTranscriptEval can use modern speech-recognition models such as **OpenAI Whisper** and **Faster-Whisper**.

## 1. OpenAI Whisper

Whisper is a Transformer-based automatic speech recognition model.

It can be configured using different model sizes depending on the available hardware.

Example:

```python
transcribe_whisper(
    audio_path,
    model_size="base"
)
```

Whisper can serve as the baseline ASR system for the study.

---

## 2. Faster-Whisper

Faster-Whisper is an optimized implementation of Whisper using CTranslate2.

It is useful when faster inference is required.

Example:

```python
transcribe_faster_whisper(
    audio_path,
    model_size="base"
)
```

The model can be used as the primary transcription engine when computational efficiency is important.

---

# 📊 Model Comparison

The same audio sample can be processed using multiple ASR models.

```text
                 Same Audio
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       Whisper           Faster-Whisper
          │                     │
          ▼                     ▼
     Transcript             Transcript
          │                     │
          └──────────┬──────────┘
                     ▼
              Reference Text
                     │
                     ▼
                Evaluation
                     │
            ┌────────┼────────┐
            ▼        ▼        ▼
           WER      CER      BLEU
```

This allows the project to investigate not only speaking conditions but also differences between ASR implementations.

---

# 📈 Transcription Evaluation

## Word Error Rate — WER

WER measures word-level transcription errors.

```text
WER =
(Substitutions + Deletions + Insertions)
/
Number of Reference Words
```

WER is one of the most important metrics for ASR evaluation.

```text
Lower WER → Better transcription
```

---

## Character Error Rate — CER

CER evaluates transcription errors at the character level.

```text
CER =
Character Edit Distance
/
Number of Reference Characters
```

CER provides a more fine-grained view of transcription errors.

```text
Lower CER → Better transcription
```

---

## BLEU

BLEU measures n-gram overlap between the generated transcript and the reference transcript.

```text
Higher BLEU → Greater textual similarity
```

Although BLEU was originally developed for machine translation evaluation, it can provide an additional similarity measure for transcript comparison.

---

## ROUGE

ROUGE measures overlap between reference and generated text using n-gram and sequence-based comparisons.

Higher ROUGE values generally indicate greater overlap with the reference transcript.

---

## METEOR

METEOR provides a word-level comparison that can consider stemming and synonym relationships.

It can provide additional information about linguistic similarity beyond exact word matching.

---

# 🧮 Evaluation Pipeline

```text
Reference Transcript
        │
        ▼
Text Normalization
        │
        ▼
ASR Model
        │
        ▼
Generated Transcript
        │
        ▼
Hypothesis Normalization
        │
        ▼
Evaluation
        │
   ┌────┼─────┬───────┬────────┐
   ▼    ▼     ▼       ▼        ▼
  WER  CER   BLEU   ROUGE   METEOR
```

The evaluation system records the metrics for every sample.

The resulting data can then be exported as a CSV file.

---

# 📁 Project Structure

```text
SpeechTranscriptEval/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│   ├── samples/
│   ├── reference_transcripts/
│   └── results/
│       └── evaluation_results.csv
│
├── docs/
│   ├── case_study.md
│   └── evaluation_metrics.md
│
├── scripts/
│   └── run_evaluation.py
│
└── src/
    ├── __init__.py
    ├── audio_processor.py
    ├── transcriber.py
    ├── metrics.py
    └── report_generator.py
```

---

# 🧩 Module Responsibilities

| Module                  | Responsibility                                        |
| ----------------------- | ----------------------------------------------------- |
| `app.py`                | Main Streamlit application and user interface         |
| `audio_processor.py`    | Audio loading, validation, extraction, and conversion |
| `transcriber.py`        | Whisper/Faster-Whisper transcription                  |
| `metrics.py`            | WER, CER, BLEU, ROUGE, and METEOR calculation         |
| `report_generator.py`   | Result aggregation, tables, and visualizations        |
| `run_evaluation.py`     | Batch transcription and evaluation                    |
| `case_study.md`         | Experimental methodology and findings                 |
| `evaluation_metrics.md` | Metric formulas and interpretation                    |

---

# ⚙️ Requirements

### Software

* Python 3.10+
* pip
* FFmpeg

### Python Dependencies

The project uses libraries such as:

```text
streamlit
pandas
matplotlib
openai-whisper
faster-whisper
jiwer
sacrebleu
rouge-score
nltk
```

Install dependencies using:

```bash
pip install -r requirements.txt
```

FFmpeg must also be installed and available from the terminal.

Verify the installation with:

```bash
ffmpeg -version
```

---

# 🚀 Installation

## 1. Clone or Download the Project

Place the project on your local machine.

```text
SpeechTranscriptEval/
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate the Environment

On Windows:

```bash
.\.venv\Scripts\Activate.ps1
```

## 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

After activating the virtual environment:

```bash
streamlit run app.py
```

The Streamlit application provides an interactive interface for:

```text
Upload Sample
     ↓
Audio Processing
     ↓
Transcription
     ↓
Reference Transcript
     ↓
Evaluation
     ↓
Results
```

---

# ⚡ Fast Transcription

For situations where only a transcript is required, Faster-Whisper can be used without performing the complete evaluation workflow.

Example:

```python
from src.transcriber import transcribe_faster_whisper

result = transcribe_faster_whisper(
    audio_path,
    model_size="base"
)
```

This provides a faster route for obtaining transcripts.

---

# 🧪 Batch Evaluation

The complete dataset can be evaluated automatically using:

```bash
python scripts/run_evaluation.py \
    --samples-dir data/samples \
    --refs-dir data/reference_transcripts \
    --out data/results/evaluation_results.csv
```

The script processes each sample, generates the transcript, compares it with the corresponding reference, calculates evaluation metrics, and stores the results.

---

# 📋 Example Result Table

After evaluation, results can be organized as:

| Sample       | Condition     | WER ↓ | CER ↓ | BLEU ↑ | ROUGE ↑ | METEOR ↑ |
| ------------ | ------------- | ----: | ----: | -----: | ------: | -------: |
| Formal 01    | Formal        |     — |     — |      — |       — |        — |
| Informal 01  | Informal      |     — |     — |      — |       — |        — |
| Clean 01     | Clean         |     — |     — |      — |       — |        — |
| Noisy 01     | Noisy         |     — |     — |      — |       — |        — |
| Interview 01 | One-on-One    |     — |     — |      — |       — |        — |
| Panel 01     | Multi-Speaker |     — |     — |      — |       — |        — |

The values are generated after the evaluation pipeline is executed.

---

# 📊 Comparative Analysis

The system aggregates individual results by condition.

For example:

| Condition     | Average WER ↓ | Average CER ↓ | Average BLEU ↑ | Average ROUGE ↑ | Average METEOR ↑ |
| ------------- | ------------: | ------------: | -------------: | --------------: | ---------------: |
| Formal        |             — |             — |              — |               — |                — |
| Informal      |             — |             — |              — |               — |                — |
| Clean         |             — |             — |              — |               — |                — |
| Noisy         |             — |             — |              — |               — |                — |
| One-on-One    |             — |             — |              — |               — |                — |
| Multi-Speaker |             — |             — |              — |               — |                — |

This makes it possible to determine which conditions produce the largest changes in transcription quality.

---

# 🔬 Research Questions

The case study can be structured around the following research questions.

### RQ1 — Speaking Style

How does formal speech compare with informal conversation in terms of ASR accuracy?

### RQ2 — Background Noise

How does background noise influence transcription performance?

### RQ3 — Speaker Interaction

Does multi-speaker interaction produce higher transcription error than one-on-one speech?

### RQ4 — Speaking Rate

Does fast speech increase WER and CER?

### RQ5 — Accent

How does accent variation influence ASR performance?

### RQ6 — Evaluation Metrics

How consistently do WER, CER, BLEU, ROUGE, and METEOR reflect changes in transcription quality?

---

# 🎯 Expected Outcome

The expected outcome is a quantitative study demonstrating how different speaking conditions influence ASR transcription quality.

The project should identify trends such as:

```text
Speaking Condition
        ↓
ASR Transcription
        ↓
Metric Calculation
        ↓
Condition-Level Average
        ↓
Comparison
        ↓
Research Finding
```

For example, noisy audio may produce higher transcription error than clean audio, while multi-speaker recordings may introduce additional errors because of speaker changes and overlapping speech.

The actual conclusions should be based on the experimental results rather than assumed in advance.

---

# 🎓 Use Cases

## Education

SpeechTranscriptEval can be used for:

* Lecture transcription
* Recorded lesson analysis
* Caption evaluation
* Educational speech research

## Business & Meetings

Potential applications include:

* Meeting transcription
* Meeting-quality evaluation
* Speaker-condition analysis
* Automatic captioning evaluation

## Interviews

The system can support:

* Interview transcription
* Interview transcript comparison
* Speech-quality research
* ASR benchmarking

## Media

The pipeline can be applied to:

* Video transcription
* Audio-to-text conversion
* Caption generation evaluation
* Broadcast speech analysis

## Research

The project can serve as a platform for:

* ASR benchmarking
* Speech-condition experiments
* Model comparison
* Evaluation-metric analysis

---

# ⚠️ Current Limitations

1. The size of the evaluation dataset can affect the reliability of conclusions.
2. Different speakers introduce natural variability.
3. Background noise may differ in intensity and type.
4. Accent effects can be difficult to isolate from speaker characteristics.
5. BLEU, ROUGE, and METEOR were not originally designed specifically for ASR evaluation.
6. WER and CER are more directly associated with speech-recognition error measurement.
7. ASR performance depends on the selected model and model size.
8. Large ASR models may require significant computational resources.
9. Reference transcripts must be accurate for meaningful evaluation.
10. Overlapping speech can be difficult for conventional transcription pipelines.
11. The study results depend on the representativeness of the selected samples.

---

# 🔮 Future Enhancements

Potential improvements include:

* Add additional ASR models
* Add multilingual speech recognition
* Add speaker diarization
* Add automatic language detection
* Add advanced noise-reduction preprocessing
* Add GPU acceleration
* Add larger evaluation datasets
* Add automated condition labeling
* Add confidence-score analysis
* Add timestamped transcripts
* Add speaker-level evaluation
* Add more advanced visualization dashboards
* Add statistical significance testing
* Add model latency benchmarking
* Add pronunciation-level analysis
* Add real-time transcription
* Add PDF/DOCX report generation
* Add automated research reports
* Add additional evaluation metrics

---

# 🧹 Temporary File Processing

During preprocessing, uploaded media may be converted into temporary WAV files.

Temporary processing can involve:

```text
Input Audio / Video
        ↓
Temporary Media File
        ↓
Converted WAV
        ↓
ASR Processing
        ↓
Transcript
```

Temporary files should be removed when they are no longer required to prevent unnecessary storage consumption.

---

# 🧯 Error Handling

The application should handle common processing failures such as:

* Unsupported audio format
* Invalid media file
* Missing FFmpeg
* Failed audio extraction
* Empty audio
* ASR model loading failure
* Transcription failure
* Missing reference transcript
* Invalid reference text
* Metric calculation errors
* Missing dataset files

Processing functions should return useful status information so that the Streamlit interface can display understandable feedback.

---

# 🔐 Data & Privacy

Speech recordings may contain personal, confidential, or sensitive information.

The project should therefore be used responsibly.

When working with real-world recordings:

* Use recordings that you are permitted to process.
* Avoid publishing private recordings.
* Protect reference transcripts and generated transcripts.
* Review storage and retention requirements.
* Remove temporary files when appropriate.
* Avoid placing confidential recordings in public repositories.

The `data/samples/` directory can be excluded from Git using `.gitignore` when the recordings should remain local.

---

# 📄 Documentation

Detailed project documentation is maintained in the `docs/` directory.

### Case Study

```text
docs/case_study.md
```

Contains:

* Research objective
* Dataset selection
* Speaking conditions
* Sample selection
* Experimental methodology
* Results
* Comparative analysis
* Discussion
* Findings
* Conclusion

### Evaluation Metrics

```text
docs/evaluation_metrics.md
```

Contains:

* WER formula
* CER formula
* BLEU explanation
* ROUGE explanation
* METEOR explanation
* Metric interpretation
* Advantages
* Limitations

---

# 📁 Data Organization

The dataset follows a simple paired structure:

```text
data/
│
├── samples/
│   ├── formal_01.mp4
│   ├── informal_01.mp4
│   ├── clean_01.wav
│   └── noisy_01.wav
│
├── reference_transcripts/
│   ├── formal_01.txt
│   ├── informal_01.txt
│   ├── clean_01.txt
│   └── noisy_01.txt
│
└── results/
    └── evaluation_results.csv
```

The matching filename allows the batch evaluation script to automatically locate the correct reference transcript.

---

# 🛠️ Technologies Used

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| **Python**         | Core programming language       |
| **Streamlit**      | Interactive web interface       |
| **OpenAI Whisper** | Baseline ASR                    |
| **Faster-Whisper** | Efficient ASR inference         |
| **FFmpeg**         | Audio extraction and conversion |
| **JiWER**          | WER and CER evaluation          |
| **SacreBLEU**      | BLEU evaluation                 |
| **ROUGE Score**    | ROUGE evaluation                |
| **NLTK**           | METEOR evaluation               |
| **Pandas**         | Data processing and aggregation |
| **Matplotlib**     | Result visualization            |

---

# 📌 Project Status

SpeechTranscriptEval provides an integrated foundation for:

```text
Media Input
     ↓
Audio Processing
     ↓
Speech Recognition
     ↓
Reference Comparison
     ↓
Metric Calculation
     ↓
Condition-Level Aggregation
     ↓
Visualization
     ↓
Comparative Analysis
     ↓
Research Findings
```

The modular architecture allows additional ASR models, metrics, preprocessing techniques, datasets, and visualization methods to be added independently.

---

# 🧠 Why Evaluate Speaking Conditions?

A single overall ASR accuracy score does not explain how a system behaves in real-world environments.

Two recordings can have the same duration and topic but produce very different transcription results because of:

```text
Speaking Style
      +
Audio Quality
      +
Speaker Interaction
      +
Accent
      +
Speaking Rate
      ↓
ASR Performance
```

Studying these factors separately provides a more useful understanding of the strengths and limitations of speech-recognition systems.

This makes SpeechTranscriptEval both a practical transcription application and an experimental research framework.

---

# 📊 Research Output

The final project produces three major forms of output.

### 1. Generated Transcripts

The ASR system produces a transcript for every selected audio/video sample.

### 2. Quantitative Metrics

Each transcript is evaluated using:

```text
WER
CER
BLEU
ROUGE
METEOR
```

### 3. Comparative Findings

Results are grouped according to speaking condition to identify meaningful differences.

The final research discussion should explain:

* Which condition produced the highest error?
* Which condition produced the best transcription?
* Which metric showed the clearest difference?
* How much did performance change between paired conditions?
* What practical implications do the findings have?

---

# 📋 Example Research Summary

```text
                Speech Samples
                       │
                       ▼
              Speaking Conditions
                       │
                       ▼
                ASR Transcription
                       │
                       ▼
             Reference Comparison
                       │
                       ▼
              Multiple Metrics
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        WER/CER      BLEU        ROUGE/METEOR
          │            │            │
          └────────────┼────────────┘
                       ▼
              Condition Comparison
                       │
                       ▼
                Research Findings
```

The final conclusion should be supported by measured results from the selected dataset.

---

# 📄 License

No license file is currently included.

If the repository is intended to become publicly reusable, an appropriate license such as the MIT License can be added.

---

# 👤 Author

**Coursework Project — Speech Transcription and Performance Evaluation**

---

# ⭐ Project Summary

SpeechTranscriptEval provides an end-to-end framework for studying the performance of Automatic Speech Recognition systems under different speaking conditions.

```text
🎙️ Audio / Video
       +
🔊 Audio Processing
       +
🤖 ASR Transcription
       +
📝 Reference Transcripts
       +
📊 Objective Evaluation
       +
🧪 Case Study Analysis
       +
📈 Visualization
       =
🔬 ASR Performance Study
```

The project combines **speech processing, Natural Language Processing, machine learning, automatic speech recognition, evaluation metrics, data analysis, and interactive application development** into a single coursework-oriented research pipeline.

**SUBMITTED BY :
NAHULAN BHARATHY K 2582434,
VYSHNAV PRASAD     2582412**

**SpeechTranscriptEval — Measuring how real-world speaking conditions affect speech transcription accuracy.**
