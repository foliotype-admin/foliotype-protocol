import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
fichier_source = SCRIPT_DIR / "hermes_synchro.wav"
fichier_conforme = SCRIPT_DIR / "hermes_synchro_cubase.wav"

print("🔄 Conversion du flux ElevenLabs en WAV PCM 24-bit / 48 kHz (Standards FolioType)...")

# Utilisation directe de FFmpeg via le système pour garantir l'encodage strict en 24-bit (pydub gère mal le 24-bit natif)
cmd = f'ffmpeg -y -i "{fichier_source}" -acodec pcm_s24le -ac 1 -ar 48000 "{fichier_conforme}"'
retour = os.system(cmd)

if retour == 0:
    print(f"✅ Fichier broadcast généré avec succès : {fichier_conforme.name}")
else:
    print("❌ ÉCHEC : Assurez-vous que FFmpeg est accessible dans votre terminal.")s