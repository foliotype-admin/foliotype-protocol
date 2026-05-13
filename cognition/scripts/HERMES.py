import os
import time
import requests
import random
import re
from pathlib import Path
from dotenv import load_dotenv

# --- 1. CONFIGURATION ET CHARGEMENT ---
# Détection dynamique de la racine du projet (foliotype-protocol)
BASE_PATH = Path(__file__).resolve().parent.parent.parent
env_path = BASE_PATH / ".env"

if env_path.exists():
    # override=True assure que les variables du fichier écrasent celles du système
    load_dotenv(dotenv_path=env_path, override=True)
else:
    print(f"❌ ERREUR CRITIQUE : Fichier .env absent à {env_path}")

API_KEY = os.getenv("ELEVEN_API_KEY")
CURRENT_VOICE_ID = os.getenv("VOICE_ID_HERMES")

# --- 2. RÉGLAGES ET PILOTAGE ---
LANGUE = 'FR' 

VOICE_CONFIG = {
    'FR': {
        'path': "docs/assets/workflow/script_source_fr.txt",
        'out': "hermes_fr_master.mp3",
        'params': {
            "stability": 0.65,
            "similarity_boost": 0.8,
            "style": 0.0,
            "speed": 1.1,
            "use_speaker_boost": True
        }
    },
    'EN': {
        'path': "docs/assets/workflow/script_source_en.txt",
        'out': "hermes_en_master.mp3",
        'params': {
            "stability": 0.5,
            "similarity_boost": 0.85,
            "style": 0.45,
            "speed": 0.9,
            "use_speaker_boost": True
        }
    }
}

# --- 3. MOTEUR RYTHMIQUE ---
def inject_natural_rhythm(text):
    def rand_sp(base):
        return " " * (base + random.randint(-3, 4))
    text = text.replace(", ", f", .{rand_sp(4)}. ")
    text = re.sub(r'\. ([A-Z])', rf'.{rand_sp(10)}. \1', text)
    paragraphs = text.split("\n\n")
    processed_paragraphs = []
    for p in paragraphs:
        if p.strip():
            processed_paragraphs.append(p.strip() + f".{rand_sp(18)}.")
    return "\n\n".join(processed_paragraphs)

# --- 4. GÉNÉRATION ---
def generate_hermes():
    if not CURRENT_VOICE_ID:
        print("❌ ÉCHEC : VOICE_ID_HERMES non détecté. Vérifiez votre fichier .env")
        return

    config = VOICE_CONFIG[LANGUE]
    script_path = BASE_PATH / config['path']
    output_dir = BASE_PATH / "cognition" / "output" / "mastered"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not script_path.exists():
        print(f"❌ SCRIPT SOURCE MANQUANT : {script_path}")
        return

    with open(script_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    final_text = inject_natural_rhythm(raw_text)
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{CURRENT_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg", 
        "Content-Type": "application/json", 
        "xi-api-key": API_KEY
    }
    
    data = {
        "text": final_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": config['params']
    }

    print(f"🌍 MODE : {LANGUE} | 🎙️ Voix : HERMES | ⚙️ Rythme actif.")
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        ts = time.strftime("%d%m_%H%M")
        # Respect strict : minuscule et underscores uniquement
        clean_out = config['out'].lower().replace(" ", "_")
        archive_name = f"{ts}_{clean_out}"
        
        with open(output_dir / clean_out, "wb") as f: 
            f.write(response.content)
        with open(output_dir / archive_name, "wb") as f: 
            f.write(response.content)
            
        print(f"✅ SUCCÈS : {archive_name}")
    else:
        print(f"❌ ÉCHEC : {response.status_code} - {response.text}")

if __name__ == "__main__":
    generate_hermes()