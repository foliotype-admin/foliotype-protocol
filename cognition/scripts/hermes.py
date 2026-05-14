import os
import time
import requests
import random
import re
from pathlib import Path
from dotenv import load_dotenv

# --- 1. CONFIGURATION ET CHARGEMENT ---
BASE_PATH = Path(__file__).resolve().parent.parent.parent
env_path = BASE_PATH / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    print(f"❌ ERREUR CRITIQUE : Fichier .env absent à {env_path}")

# Alignement strict sur les clés du fichier .env
API_KEY = os.getenv("ELEVENLABS_API_KEY") 
CURRENT_VOICE_ID = os.getenv("HERMES_VOICE_ID")

# --- 2. RÉGLAGES ET PILOTAGE ---
LANGUE = 'FR' 

VOICE_CONFIG = {
    'FR': {
        'path': "assets/workflow/script_source_fr.md",
        'out': "hermes_fr_master.mp3",
        'params': {
            "stability": 0.40,
            "similarity_boost": 0.82,
            "style": 0.45,
            "speed": 1.02,
            "use_speaker_boost": True
        }
    },
    'EN': {
        'path': "assets/workflow/script_source_en.md",
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
    def strong_pause(level):
        # Le tiret cadratin (—) force une pause beaucoup plus nette que le point
        if level == "soft":
            return " — "
        if level == "medium":
            return " — . — "
        if level == "hard":
            return " — . — . — "
        return " "

    # 1. Remplace les virgules par des pauses marquées
    text = text.replace(", ", f",{strong_pause('soft')} ")
    
    # 2. Remplace les points par des silences profonds
    text = re.sub(r'\. ([A-Z])', rf'.{strong_pause("medium")} \1', text)
    
    # 3. Pauses extrêmes entre les paragraphes
    paragraphs = text.split("\n\n")
    processed_paragraphs = []
    for p in paragraphs:
        if p.strip():
            # Ajout du tag de rupture maximale à la fin des blocs
            processed_paragraphs.append(p.strip() + strong_pause("hard"))
            
    return "\n\n".join(processed_paragraphs)

# --- 4. GÉNÉRATION ---
def generate_hermes():
    if not API_KEY or not CURRENT_VOICE_ID:
        print("❌ ÉCHEC : Variables d'environnement ELEVENLABS_API_KEY ou HERMES_VOICE_ID manquantes.")
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
        clean_out = config['out'].lower().replace(" ", "_")
        archive_name = f"{ts}_{clean_out}"
        
        from pydub import AudioSegment
        import io

        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        target_lufs = -28.0
        change_in_dbfs = target_lufs - audio.dBFS
        normalized_audio = audio.apply_gain(change_in_dbfs)
        
        normalized_audio.export(output_dir / clean_out, format="mp3")
        normalized_audio.export(output_dir / archive_name, format="mp3")
            
        print(f"✅ SUCCÈS : {archive_name} | Calibrage : {target_lufs} LUFS")
    else:
        print(f"❌ ÉCHEC : {response.status_code} - {response.text}")

if __name__ == "__main__":
    generate_hermes()