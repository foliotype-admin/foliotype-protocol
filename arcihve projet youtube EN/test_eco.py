import os
import sys
import requests
from pathlib import Path

API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "yGVILNNRQl5Mycn59l9A"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

SCRIPT_DIR = Path(__file__).resolve().parent
video_source = SCRIPT_DIR / "video_matthieu.mp4"
fichier_texte = SCRIPT_DIR / "script_source_en.md"
audio_coupe_15s = SCRIPT_DIR / "audio_15s_temp.wav"
fichier_temporaire_mp3 = SCRIPT_DIR / "hermes_temp.mp3"
fichier_final_cubase = SCRIPT_DIR / "hermes_synchro_cubase.wav"

if not video_source.exists() or not fichier_texte.exists():
    print("❌ Erreur : 'video_matthieu.mp4' ou 'script_source_en.md' introuvable.")
    sys.exit(1)

# 1. FFmpeg découpe STRICTEMENT les 15 premières secondes de la vidéo localement
print("🎬 Extraction locale et stricte des 15 premières secondes de l'audio...")
cmd_cut = f'ffmpeg -y -ss 00:00:00 -i "{video_source}" -t 15 -vn -acodec pcm_s16le -ac 1 -ar 44100 "{audio_coupe_15s}"'
os.system(cmd_cut)

# 2. Lecture d'une seule ligne du script anglais pour le test de 15s
print("📖 Lecture du début du script anglais...")
with open(fichier_texte, "r", encoding="utf-8") as f:
    lignes = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

# On prend uniquement la première phrase pour le test de 15 secondes
texte_test = lignes[0] if lignes else "Hello, this is a test using the Hermes voice."
print(f"📝 Texte envoyé à l'API (Anglais forcé) : {texte_test}")

# 3. Requête TTS Directe (Aucun ID de doublage, l'anglais sort obligatoirement)
print("⏳ Envoi à ElevenLabs (Génération synchrone)...")
payload = {
    "text": texte_test,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.58,
        "similarity_boost": 0.82
    }
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code != 200:
    print("❌ Erreur API ElevenLabs :")
    print(response.text)
    if audio_coupe_15s.exists(): os.remove(audio_coupe_15s)
    sys.exit(1)

with open(fichier_temporaire_mp3, "wb") as f:
    f.write(response.content)

# 4. Encodage aux normes Cubase
print("🔄 Encodage final en WAV PCM 24-bit / 48 kHz...")
cmd_convert = f'ffmpeg -y -i "{fichier_temporaire_mp3}" -acodec pcm_s24le -ac 1 -ar 48000 "{fichier_final_cubase}"'
os.system(cmd_convert)

# Nettoyage des fichiers temporaires
for f in [audio_coupe_15s, fichier_temporaire_mp3]:
    if f.exists(): os.remove(f)

print(f"✨ Test terminé. Fichier généré : {fichier_final_cubase.name}")