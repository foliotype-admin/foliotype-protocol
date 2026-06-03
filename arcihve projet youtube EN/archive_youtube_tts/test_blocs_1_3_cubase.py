import os
from datetime import datetime
from pathlib import Path
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from pydub.effects import normalize

# --- ANCRAGE DES CHEMINS ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR.parents[1]
OUTPUT_DIR = BASE_PATH / "cognition" / "output" / "mastered" / "production_cubase_24bit"

# --- CONFIGURATION ELEVENLABS ---
API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "HijYy7UNfppHUEYbejbw"

# Stabilité ajustée pour forcer une élocution rapide et dynamique naturelle
VOICE_SETTINGS = {"stability": 0.42, "similarity_boost": 0.95, "style": 0.0}

client = ElevenLabs(api_key=API_KEY)

# Nettoyage des mots en trop, des tirets excessifs et réduction syllabique maximale
TEXTE_ULTRA_COMPACT = (
    "My-dear-comrades HEY-THERE! Did-you-know that-France ACTUALLY-owns the "
    "oldest phil-book on-earth? Almost 4000-years. And-the-CRAZIEST-part? "
    "This-ancient-text warns-us about writing-dangers! Maybe-we-blew-it."
)

def traitement_audio_pro_propre(audio_segment):
    """ Nettoyage du gain sans aucun artefact numérique ni effet de speedup """
    # Marge de sécurité pour éviter toute saturation dans les low-mids
    audio_attenue = audio_segment - 2.5
    return normalize(audio_attenue, headroom=2.0)

def generer_sequence_complete():
    horodatage = datetime.now().strftime("%m_%d_%Hh%M")
    nom_fichier = f"test_sequence_1_3_US_{horodatage}.wav"
    
    print(f"🎙️ Génération de la bribe unique épurée : {nom_fichier}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    chemin_final = OUTPUT_DIR / nom_fichier
    chemin_temp = OUTPUT_DIR / f"temp_{nom_fichier}"
    
    try:
        audio_generator = client.text_to_speech.convert(
            voice_id=VOICE_ID, 
            text=TEXTE_ULTRA_COMPACT, 
            model_id="eleven_turbo_v2_5", 
            voice_settings=VOICE_SETTINGS
        )
        
        with open(chemin_temp, "wb") as f:
            for chunk in audio_generator: 
                f.write(chunk)
                
        audio = AudioSegment.from_file(str(chemin_temp))
        
        # Application du gain et de la normalisation sans altération temporelle
        audio = traitement_audio_pro_propre(audio)
        
        audio = audio.set_frame_rate(48000).set_channels(1).set_sample_width(3)
        audio.export(str(chemin_final), format="wav", codec="pcm_s24le")
        
        chemin_temp.unlink()
        print(f"\n✅ [SUCCÈS] Fichier audio naturel et fluide généré !")
        print(f"👉 Importe-le dans Cubase : {chemin_final.resolve()}")
    except Exception as e:
        print(f"❌ ÉCHEC : {e}")
        if chemin_temp.exists(): 
            chemin_temp.unlink()

if __name__ == "__main__": 
    generer_sequence_complete()