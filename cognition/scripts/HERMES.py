import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# --- PILOTAGE (À MODIFIER ICI) ---
# LANGUE = 'FR' 
LANGUE = 'EN'

# --- 1. CONFIGURATION ---
BASE_PATH = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_PATH / '.env'
load_dotenv(dotenv_path=ENV_PATH)
API_KEY = os.getenv("ELEVEN_API_KEY")

if not API_KEY:
    print(f"❌ ERREUR : API_KEY non détectée dans {ENV_PATH}")
    exit()
else:
    print(f"✅ PROTOCOLE : Liaison établie avec ElevenLabs")

# --- 2. CONFIGURATION DES IDENTITÉS ---
# Assurez-vous que ces IDs sont ceux de votre NOUVEAU compte
VOICE_CONFIG = {
    'FR': {
        'id': 'VOTRE_ID_HERMES_FR', 
        'script': 'script_fr.txt',
        'output': 'output/FR'
    },
    'EN': {
        'id': 'XXmoXQ8IkRfLsD1O1lKV', # ID utilisé dans votre test
        'script': 'script_en.txt',
        'output': 'output/EN'
    }
}

# --- 3. LOGIQUE DE GÉNÉRATION DYNAMIQUE ---
def generate_hermes():
    # RÉCUPÉRATION DE LA CONFIG SELON LE SWITCH
    config = VOICE_CONFIG[LANGUE]
    
    script_path = BASE_PATH / "COGNITION" / config['script']
    output_dir = BASE_PATH / config['output']
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not script_path.exists():
        print(f"❌ ERREUR : Fichier source introuvable : {script_path}")
        return

    with open(script_path, "r", encoding="utf-8") as f:
        texte = f.read()

    print(f"🌍 MODE : {LANGUE} | 📖 LECTURE : {len(texte)} caractères.")
    
    # L'URL utilise maintenant l'ID de la config choisie
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config['id']}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    
    data = {
        "text": texte,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.80}
    }

    print(f"⏳ PROPULSION HERMES ({LANGUE}) : Envoi vers ElevenLabs...")
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        timestamp = time.strftime("%Hh%M")
        # Le nom du fichier s'adapte aussi à la langue
        filename = output_dir / f"HERMES_{LANGUE}_{timestamp}_MASTER.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ SUCCÈS : Master HERMES {LANGUE} généré -> {filename}")
    else:
        print(f"❌ ÉCHEC API {LANGUE} : {response.status_code} - {response.text}")

if __name__ == "__main__":
    generate_hermes()