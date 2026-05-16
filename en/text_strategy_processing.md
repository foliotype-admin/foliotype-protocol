________________________________________________________________________________
[ SOURCE_ID: DOC-HERMES-FR-2026-V1.1 ]                   [ F O L I O T Y P E ]
________________________________________________________________________________

H E R M E S . P Y

## 1. Fonction du Script
`hermes.py` est le moteur de génération vocale par IA du studio. Il transforme les scripts textuels en fichiers audio haute fidélité (MP3 44.1kHz, 192kbps) en appliquant des profils de « personnalité acoustique » distincts.

![Moteur Hermes](../assets/scripts/hermes_core_engine.png)

## 2. Architecture Audio (Réglages de Voix)
Le script utilise deux profils de réglages optimisés pour définir l'identité sonore Foliotype :
* **Profil LEAD (EN) :** Stable et frontal (Stabilité : 0.85).
* **Profil GHOST (FR) :** Éthéré et lointain (Stabilité : 0.35). Signature « French Touch ».

## 3. Sécurisation et Métadonnées (Foliotype Secure)
Chaque fichier généré subit un scellement automatique via le module `ID3`. Le script injecte une signature de propriété intellectuelle indélébile dans les métadonnées. 
* **Signature Technique :** `FOLIOTYPE:V1.0;LANG:XX;STATUS:MASTER`

![Piste d'Audit](../assets/scripts/audit_trail.png)

## 4. Dépendances et Flux de Travail
* **Moteur :** ElevenLabs API (Modèle Multilingual v2)
* **Entrée :** `script_source_en.txt` & `script_source_fr.txt` dans [assets/workflow/](../assets/workflow/)
* **Sortie :** `docs/assets/mastering/`

---

<p align="center">
  <img src="../assets/mastering/audio_analysis/certified_mastered.png" width="600">
</p>

## 1. Metadata Injection & MP3 Integrity
The final stage of the protocol ensures that the audio asset is self-documenting. Standardized ID3 tags are injected for traceability and seamless integration with broadcasting platforms.

## 2. Attestation of Compliance
This document certifies that the audio asset has been validated under the authority of the **Foliotype Protocol**. The **Certified Mastered** seal guarantees compliance with professional broadcasting requirements.

## 3. Signal Analysis (Supervision)
* **Loudness (EBU R128):** Normalized to **-16 LUFS**.
* **Spatial Integrity:** Positive phase correlation verified.
* **Tonal Balance:** Frequency spectrum calibrated for maximum clarity.

> [!IMPORTANT]
> Technical details: [`production_validation.md`](./production_validation.md)

## 4. Origin Validation (Data Integrity)
The produced audio is certified faithful to the optimized textual sources.
* **Certified Source:** [`source_text_en.md`](./source_text_en.md)
* **Transformation Workflow:** [`text_strategy_processing.md`](./text_strategy_processing.md)

---
**STATUS:** `COMPLIANT`  
**CERTIFICATION:** `FOLIOTYPE-PROTOCOL-AUDIT-2026`  
**SIGNAL:** `PASS`

---

<p align="center">
  <a href="../README.md"><b>🏠 Back to Home</b></a>
</p>

__________________________                              __________________________
[ STATUS: CERTIFIED_TEXT_SOURCE ]                       [ CHECKSUM: VERIFIED ]

<img src="../brand/logo_foliotype.svg" width="65" valign="middle"> **F O L I O T Y P E  P R O T O C O L** | [Excellence Acoustique et Sécurisation des Métadonnées](./SUPERVISION_ANALYSIS.md)

---
**Legal Note**: This project is protected by copyright. The master sealing protocol has been subject to a prior deposit referenced in the e-Soleau register (Deposit dated 05/15/2026).
Ref: FT-20260515-INPI-SOLEAU

