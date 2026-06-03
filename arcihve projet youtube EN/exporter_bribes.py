import shutil
from pathlib import Path

# --- CHEMINS ---
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR.parents[1]
SRC_DIR = BASE_PATH / "cognition" / "output" / "mastered" / "production"

# On va créer un dossier directement sur ton Bureau pour que ce soit simple
DESKTOP_DIR = Path.home() / "Desktop" / "Bribes_Anglais_Voix"

def exporter():
    if not SRC_DIR.exists():
        print(f"❌ Le dossier source n'existe pas : {SRC_DIR}")
        return
        
    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
    fichiers = list(SRC_DIR.glob("bribe_*.wav"))
    
    print(f"📦 Copie de {len(fichiers)} fichiers audio vers votre Bureau...")
    
    for f in fichiers:
        shutil.copy(f, DESKTOP_DIR / f.name)
        
    print(f"\n🎯 [SUCCESS] Tout est prêt ! Ouvre le dossier nommé 'Bribes_Anglais_Voix' sur ton Bureau.")
    print("👉 Glisse ces fichiers un par un dans ton logiciel de montage et cale-les sur les images.")

if __name__ == "__main__":
    exporter()