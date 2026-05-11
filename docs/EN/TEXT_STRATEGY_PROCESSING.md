________________________________________________________________________________
[ SOURCE_ID: DOC-HERMES-FR-2026-V1.1 ]                   [ F O L I O T Y P E ]
________________________________________________________________________________

# <img src="../banniere.svg" width="35" valign="middle"> &nbsp; H E R M E S . P Y

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
> <img src="../banniere.svg" width="16"> **F O L I O T Y P E  P R O T O C O L** | [Excellence Acoustique et Sécurisation des Métadonnées](./SUPERVISION_ANALYSIS.md)

________________________________________________________________________________
[ STATUS: CERTIFIED_TEXT_SOURCE ]                       [ CHECKSUM: VERIFIED ]