import subprocess
from pathlib import Path

AUDIO_OUTPUT = Path("cognition/output/mastered/production/nota_bonus_brut.wav")
URL_YOUTUBE = "https://www.youtube.com/watch?v=J_5xHdMX2NU"

def extraire_audio_sans_pytorch():
    print("⏳ Extraction directe de l'audio depuis YouTube via yt-dlp...")
    
    if AUDIO_OUTPUT.exists():
        AUDIO_OUTPUT.unlink()

    # Commande yt-dlp pure pour extraire en WAV sans passer par l'écosystème torch
    commande = [
        "python", "-m", "yt_dlp",
        "-x",
        "--audio-format", "wav",
        "-o", str(AUDIO_OUTPUT),
        URL_YOUTUBE
    ]
    
    try:
        subprocess.run(commande, check=True)
        print("\n🎯 [SUCCÈS] Votre audio brut est extrait et totalement sain :")
        print(f"👉 {AUDIO_OUTPUT.resolve()}")
        print("\nVous pouvez maintenant importer ce fichier directement dans Cubase !")
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction : {e}")

if __name__ == "__main__":
    extraire_audio_sans_pytorch()