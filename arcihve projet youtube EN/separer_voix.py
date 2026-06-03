import os
import subprocess
from pathlib import Path

# On part de la racine de ton projet
RACINE_PROJET = Path(r"C:\Users\pierr\dev\foliotype-protocol")

def chercher_et_separer():
    print("🕵️‍♂️ Inspection générale du projet en cours...")
    
    fichier_trouve = None
    
    # On fouille absolument tous les sous-dossiers de foliotype-protocol
    for chemin_actuel, _, fichiers in os.walk(RACINE_PROJET):
        for fichier in fichiers:
            if fichier.lower() == "nota_bonus_source.wav":
                fichier_trouve = Path(chemin_actuel) / fichier
                break
        if fichier_trouve:
            break

    if not fichier_trouve:
        print("\n❌ Alerte rouge : Le fichier 'nota_bonus_source.wav' est INTROUVABLE dans tout le projet.")
        print(f"Vérifie qu'il n'est pas resté dans tes Téléchargements ou nommé autrement (ex: .mp3, .WAV en majuscules...).")
        return

    # On a trouvé le fichier ! On prend son dossier comme dossier de sortie
    dossier_sortie = fichier_trouve.parent
    
    print("\n🎯 TROUVÉ ! Le fichier se cachait ici :")
    print(f"👉 {fichier_trouve}")
    print("-" * 60)
    print("✅ Lancement immédiat de Demucs...")

    commande = [
        "python", "-m", "demucs",
        "--mp3",
        "--two-stems=vocals",
        "-o", str(dossier_sortie),
        str(fichier_trouve)
    ]
    
    try:
        subprocess.run(commande, check=True)
        print("\n🎯 [SUCCÈS] Séparation terminée !")
        print(f"Tes fichiers (vocals.mp3 / no_vocals.mp3) sont dans : {dossier_sortie / 'htdemucs'}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Demucs : {e}")

if __name__ == "__main__":
    chercher_et_separer()