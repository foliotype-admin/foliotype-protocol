import os
import shutil
from pathlib import Path

# On cherche partout le dossier où sont stockées tes précieuses bribes
chemins_possibles = [
    Path("cognition/output/mastered/production"),
    Path("../cognition/output/mastered/production"),
    Path("output/mastered/production"),
    Path("production")
]

dossier_source = None
for cp in chemins_possibles:
    if cp.exists() and cp.is_dir():
        dossier_source = cp
        break

# Destination forcée et ultra-visible
if os.name == 'nt':  # Si tu es sur Windows
    dossier_destination = Path("C:/Bribes_Audio_Ici")
else:  # Si tu es sur Mac/Linux
    dossier_destination = Path.home() / "Bribes_Audio_Ici"

def forcer_export():
    if not dossier_source:
        print("❌ Impossible de localiser le dossier source de vos fichiers audio.")
        print("Vérifiez le nom de vos dossiers dans VS Code.")
        return
        
    dossier_destination.mkdir(parents=True, exist_ok=True)
    fichiers = list(dossier_source.glob("bribe_*.wav"))
    
    if not fichiers:
        print(f"❓ Le dossier source a été trouvé ({dossier_source}) mais il est vide.")
        return
        
    print(f"🔍 Dossier source trouvé : {dossier_source.resolve()}")
    print(f"📦 Copie de {len(fichiers)} fichiers vers : {dossier_destination}...")
    
    for f in fichiers:
        shutil.copy(f, dossier_destination / f.name)
        
    print(f"\n🎯 [SUCCESS] Fichiers extraits de l'environnement !")
    print(f"👉 Allez directement ouvrir ce dossier : {dossier_destination}")

if __name__ == "__main__":
    forcer_export()