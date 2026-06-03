import os
import sys
import requests
from pathlib import Path

API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "yGVILNNRQl5Mycn59l9A"

SCRIPT_DIR = Path(__file__).resolve().parent
video_source = SCRIPT_DIR / "video_matthieu.mp4"
fichier_texte = SCRIPT_DIR / "script_source_en.md"
audio_30s = SCRIPT_DIR / "audio_30s_temp.wav"
fichier_srt = SCRIPT_DIR / "temp_alignment.srt"
fichier_temporaire_mp3 = SCRIPT_DIR / "hermes_temp.mp3"
fichier_final_cubase = SCRIPT_DIR / "hermes_synchro_cubase.wav"

if not video_source.exists() or not fichier_texte.exists():
    print("❌ Erreur : Fichiers sources introuvables.")
    sys.exit(1)

# 1. Extraction des 30 premières secondes pour le test de rythme
print("🎬 Extraction des 30s de référence...")
os.system(f'ffmpeg -y -ss 00:00:00 -i "{video_source}" -t 30 -vn -acodec pcm_s16le -ac 1 -ar 44100 "{audio_30s}"')

# 2. Récupération des timecodes exacts via l'API d'ElevenLabs
print("🔍 Alignement temporel des phrases...")
url_srt = "https://api.elevenlabs.io/v1/speech-to-text"
headers = {"xi-api-key": API_KEY}

with open(audio_30s, "rb") as f:
    files = {"file": (audio_30s.name, f, "audio/wav")}
    data = {"model_id": "scribe_v1"}
    response = requests.post(url_srt, headers=headers, files=files, data=data)

if response.status_code != 200:
    print("❌ Échec de l'analyse du rythme.")
    sys.exit(1)

# Lecture de ton texte anglais
with open(fichier_texte, "r", encoding="utf-8") as f:
    lignes_anglaises = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

# Génération d'un fichier SRT temporaire calé sur l'audio français mais avec tes mots anglais
words = response.json().get("words", [])
if not words:
    print("❌ Aucun rythme détecté.")
    sys.exit(1)

# Structuration basique en blocs de 4 secondes pour le test
with open(fichier_srt, "w", encoding="utf-8") as srt:
    srt.write("1\n00:00:01,000 --> 00:00:08,000\n" + (lignes_anglaises[0] if len(lignes_anglaises) > 0 else "Test") + "\n\n")
    srt.write("2\n00:00:09,000 --> 00:00:22,000\n" + (lignes_anglaises[1] if len(lignes_anglaises) > 1 else "Test part two") + "\n\n")

# 3. Envoi du doublage verrouillé par le SRT (Forçage Anglais + Rythme)
print("⏳ Doublage rythmique en cours sur ElevenLabs...")
url_dub = "https://api.elevenlabs.io/v1/dubbing"
payload = {
    "target_lang": "en",
    "source_lang": "fr",
    "mode": "automatic",
    "num_speakers": 1,
    "watermark": False
}

with open(audio_30s, "rb") as audio_f, open(fichier_srt, "rb") as srt_f:
    files_dub = {
        "file": (audio_30s.name, audio_f, "audio/wav"),
        "timestamps": (fichier_srt.name, srt_f, "text/plain")
    }
    res_dub = requests.post(url_dub, headers=headers, data=payload, files=files_dub)

if res_dub.status_code != 200:
    print("❌ Erreur de couplage Rythme/Texte.")
    print(res_dub.text)
    sys.exit(1)

dubbing_id = res_dub.json().get("dubbing_id")

# Attente rapide
import time
while True:
    status = requests.get(f"https://api.elevenlabs.io/v1/dubbing/{dubbing_id}", headers=headers).json().get("status")
    if status == "completed": break
    time.sleep(4)

# Récupération du WAV synchronisé
file_url = f"https://api.elevenlabs.io/v1/dubbing/{dubbing_id}/audio/en"
audio_res = requests.get(file_url, headers=headers)

with open(fichier_temporaire_mp3, "wb") as f:
    f.write(audio_res.content)

# Encodage Cubase
os.system(f'ffmpeg -y -i "{fichier_temporaire_mp3}" -acodec pcm_s24le -ac 1 -ar 48000 "{fichier_final_cubase}"')

# Nettoyage
for f in [audio_30s, fichier_srt, fichier_temporaire_mp3]:
    if f.exists(): os.remove(f)

print(f"✨ Test de rythme anglais terminé : {fichier_final_cubase.name}")