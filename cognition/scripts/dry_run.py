import os
import time
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURATION SOUVERAINE HERMÈS ---
# Navigation : cognition/scripts/dry_run.py -> remonte de 2 niveaux vers la racine
BASE_PATH = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_PATH / '.env'

# Chargement unique et explicite
load_dotenv(dotenv_path=ENV_PATH)

# Attribution de la clé (Nomenclature majuscule pour les constantes)
API_KEY = os.getenv("ELEVEN_API_KEY")
# ---------------------------------------

def add_metadata_simulated(file_path, title, lang_code):
    """Simule le scellage du master FP."""
    signature = f"foliotype:v1.0;lang:{lang_code.lower()};status:master"
    print(f"    📝 Scellage virtuel : {title}")
    print(f"    📝 Signature ID3 : {signature}")

def run_dry_test():
    """Exécute le protocole de test à blanc."""
    print(f"\n--- 🔒 F O L I O T Y P E : DRY RUN (PROJET: PORTEFOLIO) ---")

    if not API_KEY:
        print(f"❌ Erreur : ELEVEN_API_KEY non détectée dans {ENV_PATH}")
        return
    
    print(f"✅ [FP] Liaison établie avec .env à la racine")

    # Alignement sur l'arborescence réelle : cognition/output/mastered
    languages = ["FR", "EN"]
    
    for lang in languages:
        print(f"\n[ Configuration environnement {lang} ]")
        
        # Dossier de sortie conforme à l'arborescence du projet
        output_dir = BASE_PATH / "cognition" / "output" / "mastered"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = time.strftime("%Hh%M")
        # Nomenclature : minuscules et underscores
        test_file_name = f"hermes_{lang.lower()}_{timestamp}_test.mp3"
        
        try:
            title_tag = f"hermes_v4_{lang.lower()}_master"
            add_metadata_simulated(test_file_name, title_tag, lang)
            
            print(f"✅ Dossier vérifié : {output_dir}")
            print(f"✅ Structure prête pour : {test_file_name}")
        except Exception as e:
            print(f"❌ Échec du protocole {lang} : {e}")

    print(f"\n🚀 SYSTÈME PRÊT : Les structures sont opérationnelles.")

if __name__ == "__main__":
    run_dry_test()