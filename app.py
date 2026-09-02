"""
app.py

Streamlit interface for SpeechTranscriptEval:
Upload an audio/video sample (+ optional reference transcript),
generate an ASR transcript, and view WER/CER/BLEU/ROUGE/METEOR scores.
Also supports loading and comparing all results already saved in
data/results/evaluation_results.csv.
"""

import os
import tempfile

import pandas as pd
import streamlit as st

from src.audio_processor import convert_to_wav, validate_file
from src.transcriber import transcribe
from src.metrics import evaluate_transcription
from src.report_generator import build_results_table, summarize_by_condition

st.set_page_config(page_title="SpeechTranscriptEval", page_icon="🎙️", layout="wide")

st.title("🎙️ SpeechTranscriptEval")
st.caption("Speech Transcription and Performance Evaluation under varying speaking conditions")

tab_single, tab_batch = st.tabs(["🔍 Single Sample", "📊 Batch Results"])

# ---------------------------------------------------------------------------
# Tab 1: Single-sample transcription + evaluation
# ---------------------------------------------------------------------------
with tab_single:
    st.subheader("Transcribe a sample")

    col_left, col_right = st.columns(2)

    with col_left:
        uploaded_media = st.file_uploader(
            "Audio or video file", type=["wav", "mp3", "m4a", "flac", "ogg", "mp4", "mkv", "webm", "mov", "avi"]
        )
        backend = st.selectbox("ASR backend", ["faster-whisper", "whisper"], index=0)
        model_size = st.selectbox("Model size", ["tiny", "base", "small", "medium"], index=1)

    with col_right:
        reference_text = st.text_area(
            "Reference transcript (ground truth, optional but required for scoring)",
            height=180,
            placeholder="Paste the human-verified transcript here...",
        )
        condition_label = st.text_input(
            "Speaking condition label (optional, e.g. formal / informal / clean / noisy)"
        )

    run_button = st.button("Transcribe & Evaluate", type="primary", disabled=uploaded_media is None)

    if run_button and uploaded_media is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_media.name)[1]) as tmp:
            tmp.write(uploaded_media.read())
            tmp_path = tmp.name

        valid, msg = validate_file(tmp_path)
        if not valid:
            st.error(msg)
        else:
            with st.spinner("Standardizing audio (16kHz mono WAV)..."):
                wav_path = convert_to_wav(tmp_path)

            with st.spinner(f"Transcribing with {backend} ({model_size})..."):
                result = transcribe(wav_path, backend=backend, model_size=model_size)

            st.success("Transcription complete")
            st.markdown("**Generated transcript:**")
            st.write(result["text"])
            st.caption(f"Detected language: {result.get('language', 'unknown')} · Model: {result['model']}")

            if reference_text.strip():
                scores = evaluate_transcription(reference_text, result["text"])

                st.markdown("### Evaluation")
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("WER", f"{scores['wer']}%")
                m2.metric("CER", f"{scores['cer']}%")
                m3.metric("BLEU", scores["bleu"])
                m4.metric("ROUGE-L", scores["rougeL"])
                m5.metric("METEOR", scores["meteor"])

                if st.button("💾 Append to data/results/evaluation_results.csv"):
                    out_path = "data/results/evaluation_results.csv"
                    row = {
                        "sample": os.path.splitext(uploaded_media.name)[0],
                        "condition": condition_label or "unknown",
                        "reference": reference_text,
                        "hypothesis": result["text"],
                        **scores,
                    }
                    os.makedirs("data/results", exist_ok=True)
                    if os.path.exists(out_path):
                        df = pd.read_csv(out_path)
                        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                    else:
                        df = pd.DataFrame([row])
                    df.to_csv(out_path, index=False)
                    st.success(f"Saved to {out_path}")
            else:
                st.info("Paste a reference transcript above to compute WER/CER/BLEU/ROUGE/METEOR.")

# ---------------------------------------------------------------------------
# Tab 2: Batch results viewer (reads data/results/evaluation_results.csv)
# ---------------------------------------------------------------------------
with tab_batch:
    st.subheader("Compare results across samples")
    st.caption("Populated by scripts/run_evaluation.py, or by saving single-sample results in the first tab.")

    results_path = "data/results/evaluation_results.csv"
    if os.path.exists(results_path):
        df = pd.read_csv(results_path)
        st.dataframe(df.drop(columns=["reference", "hypothesis"], errors="ignore"), use_container_width=True)

        if "condition" in df.columns or "sample" in df.columns:
            table = build_results_table(df.to_dict("records"))
            summary = summarize_by_condition(table)
            st.markdown("### Average metrics by speaking condition")
            st.dataframe(summary, use_container_width=True)
            st.bar_chart(summary.set_index("condition")[["wer", "cer"]])
    else:
        st.info(
            "No results file found yet. Run `python scripts/run_evaluation.py` "
            "or save results from the Single Sample tab first."
        )
