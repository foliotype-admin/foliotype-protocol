import os
import re
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
video_source = SCRIPT_DIR / "video_matthieu.mp4"
audio_reference = SCRIPT_DIR / "audio_reference_temp.wav"

fichier_srt = SCRIPT_DIR / "reperes_matthieu.srt"
fichier_json = SCRIPT_DIR / "reperes_matthieu.json"

if not video_source.exists():
    print("❌ Erreur : 'video_matthieu.mp4' introuvable.")
    exit(1)

def format_srt_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

# 1. Extraction de l'audio témoin
print("🎬 Extraction de l'audio témoin...")
os.system(f'ffmpeg -y -i "{video_source}" -vn -acodec pcm_s16le -ac 1 -ar 44100 "{audio_reference}" 2>NUL')

# 2. Analyse des silences
print("🔍 Analyse des plages de parole...")
cmd_silence = f'ffmpeg -i "{audio_reference}" -af silencedetect=noise=-30dB:d=0.4 -f null - 2>&1'
output = os.popen(cmd_silence).read()

silence_starts = [float(x) for x in re.findall(r'silence_start: (\d+\.?\d*)', output)]
silence_ends = [float(x) for x in re.findall(r'silence_end: (\d+\.?\d*)', output)]

# Extraction robuste de la durée sous Windows
durée_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "{video_source}"'
raw_duration = os.popen(durée_cmd).read().strip()
total_duration = float(re.findall(r'duration=(\d+\.?\d*)', raw_duration)[0])

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
    if total_duration > current_start + 0.2:
        segments.append((current_start, total_duration))
else:
    segments.append((0.0, total_duration))

# 3. Fabrication du fichier .SRT et de la structure JSON
donnees_json = []

with open(fichier_srt, "w", encoding="utf-8") as srt_file:
    for i, (start, end) in enumerate(segments):
        # Pour le SRT
        srt_file.write(f"{i+1}\n")
        srt_file.write(f"{format_srt_time(start)} --> {format_srt_time(end)}\n")
        srt_file.write(f"Phrase {i+1}\n\n")
        
        # Pour le JSON
        donnees_json.append({
            "index": i + 1,
            "start": round(start, 2),
            "end": round(end, 2),
            "duration": round(end - start, 2)
        })

with open(fichier_json, "w", encoding="utf-8") as json_file:
    json.dump(donnees_json, json_file, indent=4, ensure_ascii=False)

if audio_reference.exists():
    os.remove(audio_reference)

print(f"✨ SUCCÈS : Fichiers '{fichier_srt.name}' et '{fichier_json.name}' créés.")