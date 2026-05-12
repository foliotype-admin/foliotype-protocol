import os
from pathlib import Path
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, TCOP, COMM, TDRC, TCON

# --- CONFIGURATION DES CHEMINS ---
# Le script détecte la racine du projet par rapport à son emplacement dans COGNITION/
base_path = Path(__file__).resolve().parent.parent
master_dir = base_path / "output" / "MASTERED"

def certifier_audio(file_path):
    """Injecte les métadonnées de certification Foliotype Protocol"""
    try:
        # Tentative d'ouverture des tags existants, sinon création
        try:
            audio = ID3(file_path)
        except:
            audio = ID3()

        # Nettoyage du nom de fichier pour le titre
        file_name = os.path.basename(file_path)
        title_tag = file_name.replace(".mp3", "")
        
        # Détection de la langue via le nom de fichier
        lang = "FR" if "_FR_" in file_name.upper() else "EN"

        # --- INJECTION DES DATA IDENTITÉ ---
        audio.add(TIT2(encoding=3, text=title_tag))           # Titre
        audio.add(TPE1(encoding=3, text="Hermès IA voice"))   # Interprète ayant participé
        audio.add(TPE2(encoding=3, text=""))                  # Interprète de l'album (VIDE)
        audio.add(TALB(encoding=3, text=""))                  # Nom de l'album (VIDE)
        
        # --- SÉCURITÉ & PROPRIÉTÉ ---
        audio.add(TCOP(encoding=3, text="© 2026 Foliotype Studio. All Rights Reserved."))
        
        # Signature technique Foliotype (Champ Commentaire)
        signature = f"FOLIOTYPE:V1.0;LANG:{lang};STATUS:CERTIFIED_MASTER;OWNER:FOLIOTYPE_PROTOCOL"
        audio.add(COMM(encoding=3, lang='fra', desc='Metadata', text=signature))
        
        # --- DATATION & GENRE ---
        audio.add(TDRC(encoding=3, text="2026"))
        audio.add(TCON(encoding=3, text="Speech/Voice-Over"))

        audio.save(file_path)
        print(f"🔒 CERTIFIÉ : {file_name} -> [Hermès IA voice]")

    except Exception as e:
        print(f"❌ Erreur lors du marquage de {file_name} : {e}")

# --- LOGIQUE D'EXECUTION ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("   FOLIOTYPE PROTOCOL - CERTIFICATION DES MASTERS")
    print("="*50)

    # Vérification de l'existence du dossier MASTERED
    if not master_dir.exists():
        os.makedirs(master_dir, exist_ok=True)
        print(f"📁 Dossier créé : {master_dir}")
        print("👉 Dépose tes exports MP3 dedans et relance le script.")
    else:
        # Scan des fichiers MP3
        fichiers_a_traiter = list(master_dir.glob("*.mp3"))
        
        if not fichiers_a_traiter:
            print(f"⚠️ Aucun fichier .mp3 trouvé dans : {master_dir}")
        else:
            print(f"🚀 Traitement de {len(fichiers_a_traiter)} fichier(s)...\n")
            for mp3_file in fichiers_a_traiter:
                certifier_audio(str(mp3_file))
            
            print("\n✅ Opération terminée. Tes fichiers sont sécurisés.")
    
    print("="*50 + "\n")