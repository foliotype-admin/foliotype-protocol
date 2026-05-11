import os
import time
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURATION SOUVERAINE HERMÈS ---
# Navigation : scripts (1) -> COGNITION (2) -> racine (3)
BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_PATH / '.env'

# Chargement avec le nom de variable EXACT
load_dotenv(dotenv_path=ENV_PATH)
API_KEY = os.getenv("ELEVEN_API_KEY")
# ---------------------------------------

API_KEY = os.getenv("ELEVEN_API_KEY")

if not API_KEY:
    print(f"❌ Erreur : ELEVEN_API_KEY non détectée dans {ENV_PATH}")
else:
    print(f"✅ PROTOCOLE : Liaison établie avec .env à la racine")

api_key = os.getenv("ELEVEN_API_KEY")
# Chargement des secrets

load_dotenv(dotenv_path=ENV_PATH)
API_KEY = os.getenv("ELEVEN_API_KEY")

def add_metadata_simulated(file_path, title, lang_code):
    """
    Simule l'ajout de métadonnées sans nécessiter la bibliothèque Mutagen.
    """
    # Ici, nous ne faisons qu'afficher l'intention pour le test à blanc
    signature = f"FOLIOTYPE:V1.0;LANG:{lang_code};STATUS:MASTER"
    print(f"   📝 Scellage virtuel : {title}")
    print(f"   📝 Signature ID3 : {signature}")

def run_dry_test():
    """
    Exécute le protocole de test à blanc pour les environnements FR et EN.
    """
    print(f"\n--- 🔒 F O L I O T Y P E : DRY RUN (PROJET: PORTEFOLIO) ---")

    if not API_KEY:
        print(f"❌ Erreur : ELEVEN_API_KEY non détectée dans {ENV_PATH}")
        return
    
    print(f"✅ PROTOCOLE : Liaison établie avec .env à la racine")

    # Liste des langues à tester
    languages = ["FR", "EN"]
    
    for lang in languages:
        print(f"\n[ Configuration de l'environnement {lang} ]")
        
        # 1. Vérification/Création des répertoires
        output_dir = BASE_PATH / "output" / lang
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = time.strftime("%Hh%M")
        test_file_name = f"HERMES_{lang}_{timestamp}_TEST.mp3"
        
        # 2. Simulation du protocole
        try:
            title_tag = f"HERMES_V4_{lang}_MASTER"
            add_metadata_simulated(test_file_name, title_tag, lang)
            
            print(f"✅ Dossier vérifié : {output_dir}")
            print(f"✅ Structure prête pour : {test_file_name}")
        except Exception as e:
            print(f"❌ Échec du protocole {lang} : {e}")

    print(f"\n🚀 SYSTÈME PRÊT : Les structures FR et EN sont opérationnelles.")

if __name__ == "__main__":
    run_dry_test()