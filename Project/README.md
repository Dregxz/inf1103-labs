# Meeting Translator

A live interpreter for a **business meeting between two parties** who speak **English, Indonesian or Chinese**.
Each sentence is spoken (or typed), transcribed to text, and **Google's Gemma model reads the text only (never
the audio), translates it into the other party's language and reads its tone**. The screen always shows the
**latest translation plus the 3 sentences before it, each with a timestamp**.

## Problem statement and target users
Corporate workers travelling overseas for a short business trips may face language barriers when communicating with local clients. Although English is commonly used for communicating with international countries, differences in language proficiency, grammar, pronunciation, and cultural expressions can still lead to misunderstandings. Employees, whether working for local or international companies, may not have enough time or a practical need to learn the local language when travelling overseas for short business trips. This can be especially challenging for SMEs, which may have fewer resources to provide extensive language training. Existing translation tools mainly translate words and sentences without considering business context, tone, pronunciation, or the intended meaning. BizLate aims to bridge this gap through an AI-assisted translation system that uses speech-to-text, language detection, and an LLM with a structured language database to analyse the user's message. It can identify unclear wording, inappropriate tone or formality, and potential translation errors before producing a clearer business-appropriate translation. The translated message can then be converted back into speech for more natural communication.

## Architecture (4 layers, 100% procedural - no classes)
    voice / text / file -> io_manager -> ai_manager -> logic_manager -> data_manager

| File | Layer | Job |
|---|---|---|
| `io_manager.py` | Input | Every user boundary: terminal `print()`/`input()` **and** all Streamlit widgets; meeting setup; validation; reading meeting files; speech-to-text (local Whisper); timestamps; formatting |
| `ai_manager.py` | AI | Builds the prompt from the sentence **plus the previous 3 sentences as context**, calls Gemma, extracts + validates the JSON, retries, never crashes |
| `logic_manager.py` | Logic | `evaluate` (which rules fired), `score` (0-100 attention score), `route` (final outcome: TENSION / CHECK / ACCEPT / REJECT) |
| `data_manager.py` | Data | Save/load `data/records.json`, per-meeting history, last-N sentences, filtering, survives missing/corrupt files |
| `app.py` | Wiring | Streamlit entry point (`streamlit run app.py`) |
| `main.py` | Wiring | Terminal entry point and the shared `process_record` pipeline |

### What the AI returns for every sentence (validated JSON)
`detected_language`, `language_confidence`, `translation`, `translation_confidence`, `tone`, `tone_confidence`,
`intensity` (1-5) and `tone_reason`; `validate_response` rejects anything that does not match. The translation and the tone note are written in the **listener's** language.

### What the AI returns for every sentence (validated JSON)
`detected_language`, `language_confidence`, `translation`, `translation_confidence`, `tone`, `tone_confidence`,
`intensity` (1-5) and `tone_reason`; `validate_response` rejects anything that does not match. The translation and the tone note are written in the **listener's** language.

### Business rules (`evaluate` -> `score` -> `route`)
- **REJECT**: empty translation, or the sentence is not English, Indonesian or Chinese.
- **TENSION**: tone is angry, frustrated or anxious **and** intensity >= 4 **and** tone confidence >= 0.7.
  The app suggests slowing down and confirming that both sides understand.
- **CHECK**: language confidence < 0.6, translation confidence < 0.6, or the speaker used a different
  language than the one set for that party (probably the wrong speaker or a bad transcription).
  The app suggests confirming with the speaker. (A sentence can be TENSION and also list these doubts.)
- **ACCEPT**: everything else.
- **Attention score** (0-100, shown next to every sentence): intensity x 10 plus a weight for the tone (angry 30, frustrated 25, anxious 20, urgent 15, sad 10, others 0).

## Using the web app (`streamlit run app.py`)
**Sidebar - Meeting setup:** meeting name, a *Start a new meeting* button, and for **Party A** and **Party B** a
name and a language (English / Indonesian / Chinese), plus the **time zone** used for timestamps
(*Auto* uses your browser's zone). Sentences with the same meeting name belong together.

