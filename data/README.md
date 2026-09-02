# Dataset

This folder holds the audio/video samples used for the case study and their matching reference transcripts.

## Folder layout

```
data/
├── samples/                # Raw audio/video files (kept out of git — see .gitignore)
├── reference_transcripts/  # Hand-verified ground-truth .txt files
└── results/                # Generated transcripts + evaluation_results.csv (output of scripts/run_evaluation.py)
```

## Naming convention

Every sample and its reference transcript must share the same base filename, and the filename should encode the speaking condition so results can be grouped automatically:

```
<condition>_<subject>_<index>.<ext>
```

Examples:

```
data/samples/formal_newsanchor_01.wav
data/reference_transcripts/formal_newsanchor_01.txt

data/samples/informal_friendschat_01.wav
data/reference_transcripts/informal_friendschat_01.txt

data/samples/clean_interview_01.wav
data/reference_transcripts/clean_interview_01.txt

data/samples/noisy_interview_01.wav
data/reference_transcripts/noisy_interview_01.txt
```

Recommended `<condition>` labels (used by `scripts/run_evaluation.py` and `src/report_generator.py` to group results):

| Label | Meaning |
|---|---|
| `formal` | Prepared/formal speech (news, presentation, lecture) |
| `informal` | Casual/spontaneous conversation |
| `clean` | Clear audio, minimal background noise |
| `noisy` | Audio with background noise (traffic, crowd, music, etc.) |
| `interview` | One-on-one interview |
| `multispeaker` | Panel / group conversation with overlapping speech |

## Reference transcripts

- Plain UTF-8 `.txt` files.
- One continuous transcript, no timestamps or speaker labels (metrics compare raw text).
- Should be produced/verified by a human, not by the ASR model being evaluated — otherwise the comparison is circular.

## Sourcing samples

Suggested sources for a small case study (respect licensing/fair-use terms of any platform you pull from):

- Publicly available interview clips (e.g. a short YouTube interview segment)
- A recorded formal talk or news clip vs. an informal podcast/conversation clip
- The same short passage read clearly, then re-recorded with added background noise, to isolate the noise variable

Keep clips short (30–90 seconds) so manual reference-transcript creation stays manageable.
