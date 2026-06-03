import os
from pathlib import Path
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from pydub.effects import low_pass_filter, high_pass_filter

# --- ANCRAGE DES CHEMINS ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR.parents[1]
OUTPUT_DIR = BASE_PATH / "cognition" / "output" / "mastered" / "production_cubase_24bit"

# --- CONFIGURATION ELEVENLABS ---
API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "HijYy7UNfppHUEYbejbw"

# Réglages validés pour l'équilibre dynamique et le piqué du grain
VOICE_SETTINGS = {"stability": 0.40, "similarity_boost": 0.93, "style": 0.10}

client = ElevenLabs(api_key=API_KEY)

# Fusion des 3 premiers blocs isosyllabiques en une seule et unique phrase narrative.
# Le Punctuation Hacking (MAJUSCULES) maintient la projection vocale tout au long du récit.
TEXTE_COMBINE = (
    "My dear comrades, HEY THERE, good day! Did you know that France ACTUALLY owns the "
    "oldest philosophy book on earth? Almost 4000 years. And the CRAZIEST part of "
    "this, is that this ancient text warns us of the dangers of heading to print. "
    "Maybe we blew it from day one, huh?"
)

def appliquer_profil_broadcast(audio_segment):
    """ Signature acoustique : Assise chaleureuse subtile + Clarté hauts-médiums """
    # 1. Subtil boost des basses (effet de proximité)
    basses = low_pass_filter(audio_segment, 150)
    audio_chaleureux = audio_segment.overlay(basses, gain_during_overlay=+1.5)
    
    # 2. Boost de présence et de clarté (2kHz - 4kHz) pour projeter la voix
    mediums_aigus = high_pass_filter(audio_chaleureux, 2000)
    audio_final = audio_chaleureux.overlay(mediums_aigus, gain_during_overlay=+1.0)
    
    return audio_final

def generer_sequence_complete():
    print("🎙️ Génération unifiée des Blocs 1, 2 et 3 (0 à 13.84s)...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    nom_fichier = "test_sequence_1_3_US.wav"
    chemin_final = OUTPUT_DIR / nom_fichier
    chemin_temp = OUTPUT_DIR / f"temp_{nom_fichier}"
    
    if chemin_final.exists():
        chemin_final.unlink()
        
    try:
        # Modèle Turbo v2.5 pour conserver un flow américain parfait d'un bout à l'autre
        audio_generator = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            text=TEXTE_COMBINE,
            model_id="eleven_turbo_v2_5", 
            voice_settings=VOICE_SETTINGS
        )
        
        with open(chemin_temp, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        # Décodage et traitement acoustique global
        audio = AudioSegment.from_file(str(chemin_temp))
        audio = appliquer_profil_broadcast(audio)
        
        # Encodage Broadcast Wave 24-bit / 48 kHz PCM Mono pour Cubase
        audio = audio.set_frame_rate(48000).set_channels(1).set_sample_width(3)
        audio.export(str(chemin_final), format="wav", codec="pcm_s24le")
        
        chemin_temp.unlink()
        print(f"\n✅ [SUCCÈS] Séquence complète générée d'un seul bloc !")
        print(f"👉 Importe le fichier au point 00:00.000 dans Cubase : {chemin_final.resolve()}")
                
    except Exception as e:
        print(f"❌ ÉCHEC de la génération globale : {e}")
        if chemin_temp.exists():
            chemin_temp.unlink()

if __name__ == "__main__":
    generer_sequence_complete()