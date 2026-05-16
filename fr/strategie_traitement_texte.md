________________________________________________________________________________
[ SOURCE_ID: DOC-HERMES-FR-2026-V1.1 ]                   [ F O L I O T Y P E ]
________________________________________________________________________________

H E R M E S . P Y

## 1. Fonction du Script
`hermes.py` est le moteur de génération vocale par IA du studio. Il transforme les scripts textuels en fichiers audio haute fidélité (MP3 44.1kHz, 192kbps) en appliquant des profils de « personnalité acoustique » distincts, adaptés à la langue cible.

![Moteur Hermes Core](../assets/scripts/hermes_core_engine.png)

## 2. Architecture Audio (Réglages de Voix)
Le script utilise deux profils de réglages optimisés pour définir l'identité sonore Foliotype :
* **Profil LEAD (EN) :** Stable et frontal (Stabilité : 0.85). Conçu pour une narration internationale autoritaire.
* **Profil GHOST (FR) :** Éthéré et lointain (Stabilité : 0.35). Apporte une signature « French Touch » plus texturée et artistique.

## 3. Sécurisation et Métadonnées (Foliotype Secure)
Chaque fichier généré subit un scellement automatique via le module `ID3`. Le script injecte une signature de propriété intellectuelle indélébile dans les métadonnées.
* **Signature Technique :** `FOLIOTYPE:V1.0;LANG:XX;STATUS:MASTER`

![Piste d'Audit](../assets/scripts/audit_trail.png)

## 4. Dépendances et Flux de Travail
* **Moteur :** ElevenLabs API (Modèle Multilingual v2)
* **Entrée :** `script_source_en.txt` & `script_source_fr.txt` dans [assets/workflow/](../assets/workflow/)
* **Sortie :** Actifs masterisés situés dans `docs/assets/mastering/`

---

<img src="../brand/logo_foliotype.svg" width="65" valign="middle"> **F O L I O T Y P E  P R O T O C O L** | [Excellence Acoustique et Sécurisation des Métadonnées](./analyse_supervision.md)
________________________________________________________________________________
[ STATUS: CERTIFIED_TEXT_SOURCE ]                       [ CHECKSUM: VERIFIED ]

**Note Légale** : Ce projet est protégé par le droit d'auteur. Le protocole de scellage des masters a fait l'objet d'un dépôt d'antériorité référencé au registre e-Soleau (Dépôt du 15/05/2026).
Ref: FT-20260515-INPI-SOLEAU