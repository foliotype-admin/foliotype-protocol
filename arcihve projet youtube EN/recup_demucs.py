import torch
import wave
from pathlib import Path
from demucs.apply import apply_model
from demucs.pretrained import get_model
import torchaudio

# Configuration des chemins
AUDIO_INPUT = Path("cognition/output/mastered/production/nota_bonus_brut.wav")
OUTPUT_DIR = Path("cognition/output/mastered/production")

def sauver_wav_natif(chemin, donnees_audio, sample_rate):
    """Sauvegarde les données en format PCM 16-bit standard via le module natif wave"""
    # Conversion des données flottantes [-1.0, 1.0] en entiers 16-bit signés
    donnees_int = (donnees_audio * 32767).clip(-32768, 32767).astype('<i2')
    
    with wave.open(str(chemin), 'wb') as wav_file:
        # Configuration : 2 canaux (Stéréo), 2 octets par échantillon (16 bits), sample_rate
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(donnees_int.tobytes())

def extraire_stems_natif():
    print("⏳ Chargement du modèle Demucs depuis votre cache...")
    model = get_model("htdemucs")
    model.cpu()
    model.eval()

    print(f"⏳ Lecture du fichier audio : {AUDIO_INPUT.name}...")
    wav, sr = torchaudio.load(str(AUDIO_INPUT))

    print("⏳ Séparation des pistes en cours (vocal / musique)...")
    ref = wav.mean(0)
    wav = (wav - ref.mean()) / ref.std()
    
    with torch.no_grad():
        sources = apply_model(model, wav[None], num_workers=1)[0]

    # htdemucs renvoie 4 sources dans l'ordre exact : [drums, bass, other, vocals]
    # format requis pour l'écriture : [samples, channels]
    vocals = sources[3].cpu().numpy().T
    
    # Mixage des pistes non-vocales (drums + bass + other) pour l'instrumental
    no_vocals = (sources[0] + sources[1] + sources[2]).cpu().numpy().T

    print("💾 Sauvegarde chirurgicale sur le disque via wave (Contournement total)...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    sauver_wav_natif(OUTPUT_DIR / "vocals.wav", vocals, sr)
    sauver_wav_natif(OUTPUT_DIR / "no_vocals.wav", no_vocals, sr)

    print("\n🎯 [SUCCÈS] Vos deux fichiers isolés sont prêts et exploitables :")
    print(f"👉 {OUTPUT_DIR / 'vocals.wav'}")
    print(f"👉 {OUTPUT_DIR / 'no_vocals.wav'}")

if __name__ == "__main__":
    extraire_stems_natif()