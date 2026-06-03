import os
import requests
from pathlib import Path

API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
# Remplace par le dernier ID affiché dans ton terminal si nécessaire
DUBBING_ID = "OgPJRAkbXo0voJaKpFYu" 

SCRIPT_DIR = Path(__file__).resolve().parent
fichier_temporaire_mp3 = SCRIPT_DIR / "hermes_temp.mp3"
fichier_final_cubase = SCRIPT_DIR / "hermes_synchro_cubase.wav"

url = f"https://api.elevenlabs.io/v1/dubbing/{DUBBING_ID}/audio/en"
headers = {"xi-api-key": API_KEY}

print(f"📡 Tentative d'extraction forcée de la piste ANGLAISE pour l'ID : {DUBBING_ID}...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open(fichier_temporaire_mp3, "wb") as f:
        f.write(response.content)
    print("✅ Flux anglais récupéré de force. Encodage 24-bit / 48 kHz...")
    
    cmd_convert = f'ffmpeg -y -i "{fichier_temporaire_mp3}" -acodec pcm_s24le -ac 1 -ar 48000 "{fichier_final_cubase}"'
    if os.system(cmd_convert) == 0:
        print(f"✨ Succès ! Fichier disponible pour Cubase : {fichier_final_cubase.name}")
    if fichier_temporaire_mp3.exists():
        os.remove(fichier_temporaire_mp3)
else:
    print(f"❌ Impossible de forcer la récupération. Code API : {response.status_code}")
    print(response.text)