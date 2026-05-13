________________________________________________________________________________
[ SOURCE_ID: DOC-DRY-RUN-FR-2026-V1.1 ]                  [ F O L I O T Y P E ]
________________________________________________________________________________

# <img src="../banniere.svg" width="35" valign="middle"> &nbsp; S I M U L A T I O N _ D R Y _ R U N

## 1. Concept du Protocole
Le **Dry Run** est une étape de simulation obligatoire avant tout export final. Il sert à valider l'intégrité de la chaîne de traitement sans mobiliser les ressources de stockage définitives.

## 2. Points de Contrôle (Checklist)
Avant de valider une session, les éléments suivants sont passés au peigne fin :
* **Routing :** Vérification qu'aucun signal ne sature les bus internes.
* **Automatisations :** Lecture complète pour détecter d'éventuels artefacts ou sauts de gain.
* **Charge CPU :** Stabilité du système pendant le rendu en temps réel.

## 3. Validation Visuelle
L'image ci-dessous illustre une configuration de test conforme aux standards du studio (Capture Terminal) :
![Simulation Dry Run](../assets/scripts/dry_run_simulation.png)

---
**STATUT :** `SIMULATION-READY`  
**PROTOCOLE :** `FOLIOTYPE-PROTOCOL-V1.0`  

---
> <img src="../banniere.svg" width="16"> **F O L I O T Y P E  P R O T O C O L** | *Assurance Qualité & Stress Test*

________________________________________________________________________________
[ STATUS: CERTIFIED_TEXT_SOURCE ]                       [ CHECKSUM: VERIFIED ]