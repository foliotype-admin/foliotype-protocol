import os
import re
import time
import shutil
import io
import requests
from pathlib import Path
from dotenv import load_dotenv
from pydub import AudioSegment

# --- 1. CONFIGURATION ET ANCRAGE STRICT DES CHEMINS ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR.parents[1] 
env_path = BASE_PATH / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

API_KEY = os.getenv("ELEVENLABS_API_KEY")
CURRENT_VOICE_ID = os.getenv("HERMES_VOICE_ID")

# --- 2. RÉGLAGES ET PILOTAGE ---
TEST_MODE = False
LANGUE = 'EN'

VOICE_CONFIG = {
    'FR': {
        'path': "assets/workflow/script_source_fr.md",
        'out_prod': "grandcontinent_prosp_fr.mp3",
        'out_test': "grandcontinent_prosp_fr_dry_run.mp3",
        'params': {
            "stability": 0.45,
            "similarity_boost": 0.88,
            "style": 0.30,
            "speed": 1.05,
            "use_speaker_boost": True
        }
    },
    'EN': {
        'path': "assets/workflow/script_source_en.md",
        'out_prod': "grandcontinent_prosp_en.mp3",
        'out_test': "grandcontinent_prosp_en_dry_run.mp3",
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
        if level == "soft": return " — "
        if level == "medium": return " — . — "
        if level == "hard": return " — . — . — "
        return " "
    text = text.replace(", ", f",{strong_pause('soft')} ")
    text = re.sub(r'\. ([A-Z])', rf'.{strong_pause("medium")} \1', text)
    paragraphs = text.split("\n\n")
    processed_paragraphs = [p.strip() + strong_pause("hard") for p in paragraphs if p.strip()]
    return "\n\n".join(processed_paragraphs)

# --- 4. MOTEUR DE VÉRIFICATION AVANT LANCEMENT ---
def verify_before_launch(mode_label, script_path, final_text):
    print("\n==================================================")
    print("📋 RECAPITULATIF DE GENERATION")
    print("==================================================")
    print(f"Mode ciblé  : {mode_label}")
    print(f"Langue      : {LANGUE}")
    print(f"Voix active : {CURRENT_VOICE_ID}")
    print(f"Source      : {script_path.name}")
    print("--------------------------------------------------")
    print("📝 TEXTE APRES INJECTION RYTHMIQUE :")
    print("--------------------------------------------------")
    print(final_text)
    print("--------------------------------------------------")
    
    confirmation = input("⚠️  Voulez-vous envoyer cette requête à l'API ElevenLabs ? (y/n) : ")
    return confirmation.lower().strip() == 'y'

# --- 5. MOTEUR DE GÉNÉRATION AUTOMATIQUE ---
def generate_hermes():
    if not API_KEY or not CURRENT_VOICE_ID:
        print("\n--- 🚨 BLOCAGE SÉCURITÉ ---")
        print(f"Chemin cherché pour le .env : {env_path.resolve()}")
        print(f"Est-ce que le fichier existe ? : {'✅ OUI' if env_path.exists() else '❌ NON'}")
        print(f"Valeur API_KEY lue : {API_KEY}")
        print(f"Valeur VOICE_ID lue : {CURRENT_VOICE_ID}")
        print("---------------------------\n")
        print("❌ ÉCHEC : Les variables d'environnement sont invalides.")
        return

    config = VOICE_CONFIG[LANGUE]
    script_path = BASE_PATH / config['path']

    if not script_path.exists():
        print(f"❌ ÉCHEC : Le fichier source n'existe pas dans : {script_path.resolve()}")
        return

    if TEST_MODE:
        output_dir = BASE_PATH / "cognition" / "output" / "mastered" /"test"
        base_file_name = config['out_test']
        mode_label = f"🔬 MODE : TEST ACTIVE [{LANGUE}]"
    else:
        output_dir = BASE_PATH / "cognition" / "output" / "mastered"
        base_file_name = config['out_prod']
        mode_label = f"👑 MODE : PRODUCTION [{LANGUE}]"

    with open(script_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    final_text = inject_natural_rhythm(raw_text)

    if not verify_before_launch(mode_label, script_path, final_text):
        print("\n❌ OPÉRATION ANNULÉE. Aucun crédit consommé, aucun fichier généré.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    backup_dir = SCRIPT_DIR / ".backup_code"
    backup_dir.mkdir(exist_ok=True)
    ts = time.strftime("%d%m_%H%M")
    current_file = Path(__file__).resolve()
    shutil.copy(current_file, backup_dir / f"{ts}_{current_file.name}")

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

    print(f"\n🚀 Requête validée. Envoi à l'API ElevenLabs...")
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # CONSTITUTION DU NOM UNIQUE POUR EMPILAGE
        unique_file_name = f"{ts}_{base_file_name}"
        
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        
        duration_ms = len(audio)
        mid_point = duration_ms // 2
        
        first_half = audio[:mid_point]
        second_half = audio[mid_point:]
        
        compensated_second_half = second_half.apply_gain(2.5)
        audio_compensated = first_half + compensated_second_half
        
        target_lufs = -28.0
        change_in_dbfs = target_lufs - audio_compensated.dBFS
        normalized_audio = audio_compensated.apply_gain(change_in_dbfs)
        
        export_path_unique = output_dir / unique_file_name

        # EXPORTATION UNIQUE (PAS DE DOUBLON COPIE)
        normalized_audio.export(export_path_unique, format="mp3")
            
        print(f"✅ ÉCRITURE PHYSIQUE RÉUSSIE :")
        print(f" -> {export_path_unique.resolve()}")
    else:
        print(f"❌ ÉCHEC API : {response.status_code} - {response.text}")

if __name__ == "__main__":
    generate_hermes()