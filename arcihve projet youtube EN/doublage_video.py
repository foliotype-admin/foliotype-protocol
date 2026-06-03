import os
import sys
import re
import requests
from pathlib import Path

API_KEY = "sk_57624d7ee1946ab31580336396b6a258d97552764bb99a70"
VOICE_ID = "yGVILNNRQl5Mycn59l9A"

# CONFIGURATION DU TEST (Réduction des frais)
DUREE_TEST_SECONDES = 15  # Ajuste ici la durée en secondes pour tes essais

SCRIPT_DIR = Path(__file__).resolve().parent
video_source = SCRIPT_DIR / "video_matthieu.mp4"
audio_extrait = SCRIPT_DIR / "audio_extrait_temp.wav"
fichier_texte = SCRIPT_DIR / "script_source_en.md"
fichier_final_cubase = SCRIPT_DIR / "hermes_synchro_cubase.wav"

if not video_source.exists() or not fichier_texte.exists():
    print("❌ Erreur : 'video_matthieu.mp4' ou 'script_source_en.md' introuvable.")
    sys.exit(1)

# 1. Extraction d'une portion ultra-courte de l'audio (-t spécifie la durée)
print(f"🎬 Extraction des {DUREE_TEST_SECONDES} premières secondes de la piste audio...")
cmd_extract = f'ffmpeg -y -i "{video_source}" -ss 00:00:00 -t {DUREE_TEST_SECONDES} -vn -acodec pcm_s16le -ac 1 -ar 44100 "{audio_extrait}"'
os.system(cmd_extract)

# 2. Détection des plages de parole sur cet échantillon
print("🔍 Analyse du rythme sur l'échantillon...")
cmd_silence = f'ffmpeg -i "{audio_extrait}" -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1'
output = os.popen(cmd_silence).read()

silence_starts = [float(x) for x in re.findall(r'silence_start: (\d+\.?\d*)', output)]
silence_ends = [float(x) for x in re.findall(r'silence_end: (\d+\.?\d*)', output)]

segments = []
current_start = 0.0

if silence_starts and silence_ends:
    if silence_starts[0] == 0.0:
        current_start = silence_ends[0]
        silence_starts.pop(0)
        silence_ends.pop(0)
    
    for start, end in zip(silence_starts, silence_ends):
        if start > current_start + 0.2:
            segments.append((current_start, start))
        current_start = end
    
    if float(DUREE_TEST_SECONDES) > current_start + 0.2:
        segments.append((current_start, float(DUREE_TEST_SECONDES)))
else:
    segments.append((0.0, float(DUREE_TEST_SECONDES)))

# 3. Lecture et limitation du script à l'échantillon de test
with open(fichier_texte, "r", encoding="utf-8") as f:
    lignes_angles = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

# On ne garde que le nombre de lignes correspondant aux segments trouvés dans les 15s
lignes_angles = lignes_angles[:len(segments)]

# 4. Création du fichier de silence master pour la durée du test
os.system(f'ffmpeg -y -f lavfi -i anullsrc=r=48000:cl=mono -t {DUREE_TEST_SECONDES} -acodec pcm_s24le "{fichier_final_cubase}"')

# 5. Génération TTS économique
print(f"⏳ Traitement de {len(segments)} blocs sur l'échantillon économique...")
tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

for i, (start, end) in enumerate(segments):
    texte = lignes_angles[i]
    if not texte:
        continue
        
    payload = {
        "text": texte,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.58, "similarity_boost": 0.82}
    }
    
    res = requests.post(tts_url, headers=headers, json=payload)
    if res.status_code == 200:
        temp_mp3 = SCRIPT_DIR / f"temp_{i}.mp3"
        temp_wav = SCRIPT_DIR / f"temp_{i}.wav"
        
        with open(temp_mp3, "wb") as f:
            f.write(res.content)
            
        os.system(f'ffmpeg -y -i "{temp_mp3}" -acodec pcm_s24le -ac 1 -ar 48000 "{temp_wav}"')
        
        delay_ms = int(start * 1000)
        os.system(f'ffmpeg -y -i "{fichier_final_cubase}" -i "{temp_wav}" -filter_complex "[1:a]adelay={delay_ms}[aud];[0:a][aud]amix=inputs=2:duration=first" "{SCRIPT_DIR / "master_mix.wav"}"')
        
        if (SCRIPT_DIR / "master_mix.wav").exists():
            os.replace(SCRIPT_DIR / "master_mix.wav", fichier_final_cubase)
            
        if temp_mp3.exists(): os.remove(temp_mp3)
        if temp_wav.exists(): os.remove(temp_wav)

if audio_extrait.exists():
    os.remove(audio_extrait)

print(f"✨ Échantillon de test généré : '{fichier_final_cubase.name}' (Frais réduits au minimum).")