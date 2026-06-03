import os
import time
from pathlib import Path
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# --- ANCRAGE DES CHEMINS ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR.parents[1]
OUTPUT_DIR = BASE_PATH / "cognition" / "output" / "mastered" / "production_cubase_24bit"

# --- CONFIGURATION ELEVENLABS ---
API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "HijYy7UNfppHUEYbejbw"

# Mêmes réglages stricts pour conserver exactement la même clarté
VOICE_SETTINGS = {"stability": 0.52, "similarity_boost": 0.95, "style": 0.0}

client = ElevenLabs(api_key=API_KEY)

# Découpage et adaptation US des bribes 05 à 10 (00:13.840 --> 00:49.000)
SEGMENTS_SUITE = {
    "bribe_rectif_01_v2.wav": "my dear comrades! good morning to you all!",
    
}

def generer_suite():
    print("🎙️ Lancement de la génération de la suite (Bribes 05 à 10)...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for nom_fichier, texte in SEGMENTS_SUITE.items():
        chemin_final = OUTPUT_DIR / nom_fichier
        chemin_temp = OUTPUT_DIR / f"temp_{nom_fichier}"
        
        if chemin_final.exists():
            chemin_final.unlink()
            
        print(f"⏳ Génération de {nom_fichier}...")
        
        try:
            audio_generator = client.text_to_speech.convert(
                voice_id=VOICE_ID,
                text=texte,
                model_id="eleven_turbo_v2_5", 
                voice_settings=VOICE_SETTINGS
            )
            
            with open(chemin_temp, "wb") as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            # Conversion 24-bit / 48 kHz Mono pour Cubase
            audio = AudioSegment.from_file(str(chemin_temp))
            audio = audio.set_frame_rate(48000).set_channels(1).set_sample_width(3)
            audio.export(str(chemin_final), format="wav", codec="pcm_s24le")
            
            chemin_temp.unlink()
            print(f"   ✅ [OK] {nom_fichier} généré avec succès.")
            
            # Sécurité anti-alternance clair/mat
            if nom_fichier != "bribe_rectif_10.wav":
                print("   ⏳ Pause de réinitialisation de 3 secondes...")
                time.sleep(3)
                    
        except Exception as e:
            print(f"   ⚠️ ÉCHEC pour {nom_fichier} : {e}")
            if chemin_temp.exists():
                chemin_temp.unlink()
            continue

    print(f"\n🎯 Suite terminée ! Les fichiers 05 à 10 sont prêts dans : {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    generer_suite()