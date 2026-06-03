import os
import sys
import re
import requests
from pathlib import Path

API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "yGVILNNRQl5Mycn59l9A"

DUREE_TEST_SECONDES = 204

SCRIPT_DIR = Path(__file__).resolve().parent
video_source = SCRIPT_DIR / "video_matthieu.mp4"
fichier_texte = SCRIPT_DIR / "script_source_en.md"
fichier_final_cubase = SCRIPT_DIR / f"hermes_synchro_cubase_{DUREE_TEST_SECONDES}s.wav"

if not video_source.exists() or not fichier_texte.exists():
    print("❌ Erreur : 'video_matthieu.mp4' ou 'script_source_en.md' introuvable.")
    sys.exit(1)

# 1. Lecture et découpage par phrases propres
with open(fichier_texte, "r", encoding="utf-8") as f:
    texte_complet = f.read()

phrases = re.split(r'(?<=[.!?])\s+', texte_complet)
phrases = [p.strip() for p in phrases if p.strip() and not p.strip().startswith("#")]

phrases_test = phrases

# 2. Création de la piste de base Cubase (silence absolu calé sur la vidéo totale)
os.system(f'ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=mono -t {DUREE_TEST_SECONDES} -acodec pcm_s16le "{fichier_final_cubase}"')

# 3. Génération TTS et positionnement bout à bout dynamique
print(f"⏳ Génération de {len(phrases_test)} phrases avec lissage du volume...")
tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

temps_accumulation_secondes = 0.0
SILENCE_ENTRE_PHRASES = 1.5

for i, phrase in enumerate(phrases_test):
    print(f"🎙️ Génération phrase {i+1}/{len(phrases_test)} : {phrase[:50]}...")
    
    payload = {
        "text": phrase,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.65, "similarity_boost": 0.82}
    }
    
    res = requests.post(tts_url, headers=headers, json=payload)
    if res.status_code == 200:
        temp_mp3 = SCRIPT_DIR / f"temp_{i}.mp3"
        temp_wav = SCRIPT_DIR / f"temp_{i}.wav"
        
        with open(temp_mp3, "wb") as f:
            f.write(res.content)
            
        os.system(f'ffmpeg -y -i "{temp_mp3}" -acodec pcm_s16le -ac 1 -ar 48000 "{temp_wav}"')
        
        durée_genérée_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "{temp_wav}"'
        raw_duration = os.popen(durée_genérée_cmd).read().strip()
        
        try:
            durée_réelle = float(re.findall(r'(\d+\.?\d*)', raw_duration)[0])
        except IndexError:
            durée_réelle = 5.0
            
        delay_ms = int(temps_accumulation_secondes * 1000)
        
        # Correction de la ligne scindée
        os.system(f'ffmpeg -y -i "{fichier_final_cubase}" -i "{temp_wav}" -filter_complex "[1:a]adelay={delay_ms}|{delay_ms}[aud];[0:a][aud]amix=inputs=2:duration=first:normalize=0" "{SCRIPT_DIR / "master_mix.wav"}"')
        
        if (SCRIPT_DIR / "master_mix.wav").exists():
            os.replace(SCRIPT_DIR / "master_mix.wav", fichier_final_cubase)
            
        temps_accumulation_secondes += durée_réelle + SILENCE_ENTRE_PHRASES
        
        for f in [temp_mp3, temp_wav]:
            if f.exists(): os.remove(f)
    else:
        print(f"❌ Échec de génération pour la phrase {i+1}")

print(f"✨ RENDU COMPLET READY : '{fichier_final_cubase.name}'")