import os
from pathlib import Path

# --- ANCRAGE DES CHEMINS ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR.parents[1]
AUDIO_FR_PATH = BASE_PATH / "assets" / "workflow" / "audio_francais.wav"
OUTPUT_TEXT_PATH = BASE_PATH / "cognition" / "output" / "transcription_source.txt"

def installer_dependances_si_besoin():
    try:
        import speech_recognition as sr
    except ImportError:
        print("📦 Installation de la bibliothèque de transcription...")
        os.system("pip install SpeechRecognition pydub")

def transcrire_audio_francais():
    installer_dependances_si_besoin()
    import speech_recognition as sr
    
    print(f"🔍 Analyse du fichier source : {AUDIO_FR_PATH.name}...")
    
    if not AUDIO_FR_PATH.exists():
        print(f"❌ ÉCHEC : Le fichier {AUDIO_FR_PATH} est introuvable.")
        return

    recognizer = sr.Recognizer()
    
    # Lecture du fichier audio
    with sr.AudioFile(str(AUDIO_FR_PATH)) as source:
        print("⏳ Extraction du flux audio (cela peut prendre une minute)...")
        audio_data = recognizer.record(source)
        
    try:
        print("🧠 Transcription en cours via le moteur de reconnaissance...")
        texte_transcrit = recognizer.recognize_google(audio_data, language="fr-FR")
        
        # Sauvegarde du résultat
        OUTPUT_TEXT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_TEXT_PATH, "w", encoding="utf-8") as f:
            f.write(texte_transcrit)
            
        print(f"\n🎯 [SUCCESS] Transcription terminée avec succès !")
        print(f"📝 Le texte complet a été sauvegardé ici : {OUTPUT_TEXT_PATH.relative_to(BASE_PATH)}")
        print("\n--- APERÇU DU TEXTE DÉTECTÉ ---")
        print(texte_transcrit[:500] + "...")
        
    except sr.UnknownValueError:
        print("❌ ÉCHEC : Le moteur n'a pas pu comprendre l'audio. Le fichier est-il corrompu ou trop faible ?")
    except sr.RequestError as e:
        print(f"❌ ÉCHEC : Erreur de service réseau ({e})")

if __name__ == "__main__":
    transcrire_audio_francais()