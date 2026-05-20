import os
import re
import time
import shutil
import io
import json
import requests
import spacy
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
FICHIER_EXCLUSIONS = SCRIPT_DIR / "exclusions_liaisons.json"
PRESET_PATH = BASE_PATH / "assets/presets/shorts_b2b_fast.json"

# Chargement unique du modèle linguistique français
nlp = spacy.load("fr_core_news_sm")

# --- 2. RÉGLAGES ET PILOTAGE ---
TEST_MODE = False
LANGUE = 'FR'  # Basculer ici entre 'FR' et 'EN'

VOICE_CONFIG = {
    'FR': {
        'path': "assets/workflow/script_source_fr.md",
        'out_prod': "grandcontinent_prosp_fr.wav",
        'out_test': "grandcontinent_prosp_fr_dry_run.wav",
        'params': {
            "stability": 0.58,
            "similarity_boost": 0.82,
            "style": 0.26,
            "speed": 1.09,
            "use_speaker_boost": True
        }
    },
    'EN': {
        'path': "assets/workflow/script_source_en.md",
        'out_prod': "grandcontinent_prosp_en.wav",
        'out_test': "grandcontinent_prosp_en_dry_run.wav",
        'params': {
            "stability": 0.5,
            "similarity_boost": 0.85,
            "style": 0.45,
            "speed": 0.9,
            "use_speaker_boost": True
        }
    }
}

# --- 3. PRESET ET RÉGLAGES MOTEUR ---
def charger_preset(chemin: Path = PRESET_PATH) -> dict:
    if not chemin.exists():
        raise FileNotFoundError(f"Preset introuvable : {chemin.resolve()}")
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)

def voice_settings_depuis_preset(preset: dict) -> dict:
    eng = preset.get("engine_settings", {})
    settings = {
        "stability": eng["stability"],
        "similarity_boost": eng["similarity_boost"],
    }
    if "style_exaggeration" in eng:
        settings["style"] = eng["style_exaggeration"]
    if "speaker_boost" in eng:
        settings["use_speaker_boost"] = eng["speaker_boost"]
    return settings

def appliquer_speed_factor(audio: AudioSegment, factor: float) -> AudioSegment:
    if factor == 1.0:
        return audio
    altered = audio._spawn(
        audio.raw_data,
        overrides={"frame_rate": int(audio.frame_rate * factor)},
    )
    return altered.set_frame_rate(audio.frame_rate)

# --- 4. MOTEUR ANTI-LIAISONS DISGRACIEUSES ET NORMALISATION NUMÉRIQUE ---
def charger_exclusions() -> dict:
    if FICHIER_EXCLUSIONS.exists():
        with open(FICHIER_EXCLUSIONS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def ajouter_exclusion_manuelle(mot_gauche: str, mot_droite: str, prononciation: str):
    exclusions = charger_exclusions()
    exclusions[f"{mot_gauche.lower()} {mot_droite.lower()}"] = prononciation
    with open(FICHIER_EXCLUSIONS, "w", encoding="utf-8") as f:
        json.dump(exclusions, f, ensure_ascii=False, indent=4)

def corriger_liaisons_disgracieuses(texte: str) -> str:
    # --- BLOC DE NORMALISATION GÉNÉRIQUE (FR & EN) POUR ELEVENLABS ---
    # Fix des décimales coupées pour les pourcentages (ex: 63,8% ou 63.8%)
    texte = re.sub(r'(\d+),(\d+)', r'\1.\2', texte)
    
    if LANGUE == 'EN':
        # Normalisation spécifique pour le moteur anglophone
        texte = texte.replace("%", " percent")
        texte = re.sub(r'\bAI\b', 'A.I.', texte)
        texte = re.sub(r'(\d+)-(\d+)', r'\1 to \2', texte)
        return texte

    if LANGUE == 'FR':
        # Normalisation spécifique pour le moteur francophone
        texte = re.sub(r'\b20\b', 'vint', texte)
        texte = texte.replace("%", " pour cent")
        texte = re.sub(r'\b1er\b', 'premier', texte)
        texte = re.sub(r'\b(\d+)e\b', r'\1ième', texte)
        texte = re.sub(r'\b2000\b', 'deux mille', texte)
        texte = re.sub(r'\b2025\b', 'deux mille vingt-cinq', texte)
        texte = re.sub(r'\b2026\b', 'deux mille vingt-six', texte)
        texte = re.sub(r'\bIA\b', 'I.A.', texte)
        texte = re.sub(r'\bENS\b', 'É.N.S.', texte)
        texte = re.sub(r'(\d+)-(\d+)', r'\1 à \2', texte)
        
        exclusions = charger_exclusions()
        doc = nlp(texte)
        mots_modifies = [token.text for token in doc]

        for i in range(len(doc) - 1):
            mot_gauche = doc[i]
            mot_droite = doc[i+1]
            paire_cle = f"{mot_gauche.text.lower()} {mot_droite.text.lower()}"
            
            if paire_cle in exclusions:
                idx = mot_gauche.i
                mots_modifies[idx] = exclusions[paire_cle].split()[0]
                mots_modifies[idx+1] = exclusions[paire_cle].split()[1]
                continue

            if mot_gauche.pos_ == "VERB" and "Number=Plur" in str(mot_gauche.morph):
                if mot_droite.pos_ in ["ADP", "DET"]:
                    idx = mot_gauche.i
                    if mots_modifies[idx].endswith("s"):
                        mots_modifies[idx] = mots_modifies[idx][:-1]
                    elif mots_modifies[idx].endswith("x"):
                        mots_modifies[idx] = mots_modifies[idx][:-1]

        texte_corrige = ""
        for token in doc:
            texte_corrige += mots_modifies[token.i] + token.whitespace_
        return texte_corrige
        
    return texte

# --- 5. MOTEUR RYTHMIQUE ---
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

# --- 6. MOTEUR DE VÉRIFICATION AVANT LANCEMENT ---
def verify_before_launch(mode_label, script_path, final_text, preset: dict, voice_settings: dict, speed_factor: float):
    print("\n==================================================")
    print("📋 RECAPITULATIF DE GENERATION (STANDARDS FOLIOTYPE)")
    print("==================================================")
    print(f"Mode ciblé  : {mode_label}")
    print(f"Langue      : {LANGUE}")
    print(f"Voix active : {CURRENT_VOICE_ID}")
    print(f"Source      : {script_path.name}")
    print(f"Format API  : WAV de qualité studio (48 kHz)")
    print(f"Preset      : {preset.get('preset_name', PRESET_PATH.name)}")
    print(f"Stability   : {voice_settings['stability']}")
    print(f"Similarity  : {voice_settings['similarity_boost']}")
    print(f"Speed post  : x{speed_factor}")
    print("--------------------------------------------------")
    print("📝 TEXTE APRES INJECTION RYTHMIQUE :")
    print("--------------------------------------------------")
    print(final_text)
    print("--------------------------------------------------")
    
    confirmation = input("⚠️  Voulez-vous envoyer cette requête à l'API ElevenLabs ? (y/n) : ")
    return confirmation.lower().strip() == 'y'

# --- 7. MOTEUR DE GÉNÉRATION AUTOMATIQUE ---
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

    try:
        preset = charger_preset()
    except FileNotFoundError as e:
        print(f"❌ ÉCHEC : {e}")
        return

    voice_settings = voice_settings_depuis_preset(preset)
    speed_factor = preset.get("audio_pacing", {}).get("speed_factor", 1.0)

    config = VOICE_CONFIG[LANGUE]
    script_path = BASE_PATH / config['path']

    if not script_path.exists():
        print(f"❌ ÉCHEC : Le fichier source n'existe pas dans : {script_path.resolve()}")
        return

    if TEST_MODE:
        output_dir = BASE_PATH / "cognition" / "output" / "mastered" / "test"
        base_file_name = config['out_test']
        mode_label = f"🔬 MODE : TEST ACTIVE [{LANGUE}]"
    else:
        output_dir = BASE_PATH / "cognition" / "output" / "mastered" / "production"
        base_file_name = config['out_prod']
        mode_label = f"👑 MODE : PRODUCTION [{LANGUE}]"

    with open(script_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    text_sans_liaisons = corriger_liaisons_disgracieuses(raw_text)
    final_text = inject_natural_rhythm(text_sans_liaisons)

    if not verify_before_launch(mode_label, script_path, final_text, preset, voice_settings, speed_factor):
        print("\n❌ OPÉRATION ANNULÉE. Aucun crédit consommé, aucun fichier généré.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    backup_dir = SCRIPT_DIR / ".backup_code"
    backup_dir.mkdir(exist_ok=True)
    ts = time.strftime("%d%m_%H%M")
    current_file = Path(__file__).resolve()
    shutil.copy(current_file, backup_dir / f"{ts}_{current_file.name}")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{CURRENT_VOICE_ID}?output_format=wav_48000"
    headers = {
        "Accept": "audio/wav",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    data = {
        "text": final_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": voice_settings,
    }

    print(f"\n🚀 Requête validée. Envoi à l'API ElevenLabs (Flux WAV non compressé 48kHz)...")
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        unique_file_name = f"{ts}_{base_file_name}"
        
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="wav")
        audio = appliquer_speed_factor(audio, speed_factor)

        chunk_length_ms = 15000  
        chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        reference_dbfs = chunks[0].dBFS if chunks else audio.dBFS
        
        compensated_chunks = []
        for chunk in chunks:
            if len(chunk) < 2000:
                compensated_chunks.append(chunk)
                continue
                
            gain_to_apply = reference_dbfs - chunk.dBFS
            gain_to_apply = max(min(gain_to_apply, 4.0), -4.0)
            
            compensated_chunks.append(chunk.apply_gain(gain_to_apply))
        
        audio_compensated = sum(compensated_chunks, AudioSegment.empty())
        
        target_lufs = -28.0
        change_in_dbfs = target_lufs - audio_compensated.dBFS
        normalized_audio = audio_compensated.apply_gain(change_in_dbfs)
        
        export_path_unique = output_dir / unique_file_name
        
        fmt = "mp3" if unique_file_name.endswith(".mp3") else "wav"
        params = ["-acodec", "libmp3lame"] if fmt == "mp3" else ["-acodec", "pcm_s24le"]
        
        normalized_audio.export(
            export_path_unique, 
            format=fmt, 
            parameters=params
        )
            
        print(f"✅ ÉCRITURE PHYSIQUE MASTER RÉUSSIE ({export_path_unique.suffix.upper()}) :")
        print(f" -> {export_path_unique.resolve()}")
    else:
        print(f"❌ ÉCHEC API : {response.status_code} - {response.text}")

if __name__ == "__main__":
    generate_hermes()