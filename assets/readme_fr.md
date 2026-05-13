________________________________________________________________________________
[ source_id: assets-readme-fr-2026-v1.1 ]                 [ f o l i o t y p e ]
________________________________________________________________________________

<div align="center">
  <img src="assets/banniere_preview.gif" width="100%" style="border-radius: 8px;">

  <br><br>

  <img src="brand/foliotype_mark.svg" width="40">
</div>

## 1. portée
ce répertoire centralise les ressources dynamiques, les démonstrations et les médias prêts pour la diffusion. il sert de bibliothèque de rendu principale pour le **protocole foliotype**.

## 2. structure du répertoire
l'organisation est sectorisée par type de média pour optimiser l'accès et le déploiement :

* **videos/** : captures de démo, cinématiques et bannières animées (.mp4).
* **images/** : rendus de scènes, captures système et ressources ui (.png, .jpg).
* **demos/** : applications concrètes du système de conception.

## 3. protocole de gestion et d'optimisation
1. **performance web** : chaque fichier `.mp4` doit être compressé via le codec h.264 avant intégration pour garantir une lecture fluide.
2. **convention de nommage** : application stricte des `minuscules_et_underscores` (ex: `demo_interface_v1.mp4`).
3. **séparation des sources** : les fichiers projets éditables (after effects, etc.) sont proscrits ici ; ils résident exclusivement dans le dossier racine `masters/`.

---
## 4. maintenance et intégrité
* **seuil de synchronisation** : poids maximum recommandé de 50 mo par fichier.
* **validation** : toutes les nouvelles ressources doivent être testées sur la branche `preflight`.

---
> <img src="brand/foliotype_mark.svg" width="16"> **p r o t o c o l e  f o l i o t y p e** | bibliothèque de ressources dynamiques

________________________________________________________________________________
[ statut : bibliotheque_ressources ]                    [ acces : illimité ]