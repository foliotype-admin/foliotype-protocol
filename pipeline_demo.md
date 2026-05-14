# 🎧 Foliotype Protocol : Pipeline Demonstration

<p align="center">
  <img src="https://github.com/pierrentsama/foliotype-protocol/raw/master/brand/banniere.svg" width="100%">
</p>

---

## 🔍 01. Audit et Intégrité
Avant tout traitement, le signal subit un audit complet pour garantir l'absence de corruption numérique.

<table width="100%">
  <tr>
    <td width="50%">
      <b>Processus d'ingestion :</b><br>
      • Extraction des métadonnées.<br>
      • Vérification de la structure du conteneur.<br>
      • Analyse de la cohérence binaire.
    </td>
    <td width="50%">
      <img src="./assets/mastering/signal_audit.png" width="100%">
    </td>
  </tr>
</table>

---

<p align="center">
  <img src="./assets/mastering/audio_analysis/lufs_standard.png" width="80%">
</p>

<p align="center">
  <img src="./assets/mastering/audio_analysis/spectrogram.png" width="80%">
  <br><i>Analyse fréquentielle et contrôle de phase</i>
</p>

---

## 03. Pipeline Cognition
Chaque étape est pilotée par le moteur `hermes.py` situé dans `/cognition/scripts/`.

*   **Automatisation** : Scripting Python pour une reproductibilité totale.
*   **Validation** : Le script `certified_mastered.py` génère le sceau de conformité.

<p align="center">
  <img src="./assets/scripts/hermes_core_engine.png" width="900">
</p>

---

### 📂 Documentation Technique
*   [📄 Analyse Audio détaillée](./fr/analyse_audio.md)
*   [📜 Certification Master](./fr/certification_master.md)
*   [✅ Production Validation](./fr/production_validation.md)

---
<p align="center">
  <a href="./README.md"><b>🏠 Retour à l'accueil</b></a>
</p>