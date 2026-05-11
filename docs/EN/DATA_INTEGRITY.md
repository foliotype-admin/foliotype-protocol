________________________________________________________________________________
[ SOURCE_ID: DOC-DATA-INTEGRITY-EN-2026-V1.1 ]           [ F O L I O T Y P E ]
________________________________________________________________________________

# <img src="../banniere.svg" width="35" valign="middle"> &nbsp; D A T A _ I N T E G R I T Y

## 1. Source Transparency
The **Hermes AI Voice** system is built on an "Open Source" policy. Under the authority of the **Foliotype Protocol**, we expose textual source files (EN/FR) to ensure full traceability between the raw text and the generated speech synthesis.

## 2. Script Repository (Bilingual)
The files listed below represent the logical structure used by the engine. They define the prosody, rhythm, and voice parameters certified by the protocol.

* **Configuration Script:** [`scripts/DRY_RUN.py`](../../DRY_RUN.py)
* **Technical Architecture:** ![Hermes Core](../assets/scripts/hermes_core_engine.png)

## 3. The Text-to-Voice Transformation Process
Rendering quality relies on the transition from "visual" text to "vocal" text (Phonetic Optimization).

### Step 1: Raw Source Text (.txt)
The original content as designed for standard reading. These files are the pillars of the semantic audit.
* **FR Source:** [script_source_fr.txt](../assets/workflow/script_source_fr.txt)
* **EN Source:** [script_source_en.txt](../assets/workflow/script_source_en.txt)

### Step 2: Phonetic Optimization & Logic
Text is reworked for diction via Cursor automation. This stage adapts punctuation to guide the AI toward human intonation.
* **Objective:** Eliminate robotic character through auditory layout.
* **Visual Audit:** ![Audit Trail](../assets/scripts/audit_trail.png)

---

## 4. Quality Commitment
Exposing these files demonstrates the rigor of the **Foliotype Protocol**:
1.  **Absence of Bias:** Source texts are immutable and verifiable.
2.  **Surgical Precision:** Every punctuation mark is directly correlated to an inflection in the final rendering.
3.  **Data Source:** ![Data Source](../assets/scripts/data_source.png)

### 5. Nature of the Vocal Asset
The **Hermes AI Voice** engine is based on a high-fidelity cloning model derived from a corpus of **95 minutes of real audio data**.
* **Fidelity:** High phonetic resolution.
* **Ethics:** Usage strictly limited to the framework defined by the **Foliotype Protocol**.
* **Control:** Systematic signal auditing to eliminate synthesis artifacts.

---
**STATUS:** `DATA-VERIFIED`  
**PROTOCOL:** `FOLIOTYPE-PROTOCOL-V1.0`  

---
> <img src="../banniere.svg" width="16"> **F O L I O T Y P E  P R O T O C O L** | [Acoustic Compliance & Data Transparency](./AUDIO_ANALYSIS.md)

________________________________________________________________________________
[ STATUS: CERTIFIED_TEXT_SOURCE ]                       [ CHECKSUM: VERIFIED ]