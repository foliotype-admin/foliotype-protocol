import json
import math
from pathlib import Path

def format_srt_time(seconds):
    """Convertit un temps en secondes au format standard SRT : HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - math.floor(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

def json_to_srt(json_path, srt_path, words_per_block=4):
    """Convertit le fichier d'alignement de caractères ElevenLabs en fichier .srt propre"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chars = data["characters"]
    starts = data["character_start_times_seconds"]
    ends = data["character_end_times_seconds"]
    
    words = []
    current_word = ""
    word_start = None
    last_end = 0.0
    
    # 1. Reconstruction des mots complets et de leurs timings individuels
    for c, start, end in zip(chars, starts, ends):
        if c.strip() == "":
            if current_word:
                words.append({"text": current_word, "start": word_start, "end": last_end})
                current_word = ""
                word_start = None
        else:
            if word_start is None:
                word_start = start
            current_word += c
            last_end = end
            
    if current_word:
        words.append({"text": current_word, "start": word_start, "end": last_end})

    # 2. Groupement des mots en blocs rythmiques pour la timeline vidéo
    with open(srt_path, 'w', encoding='utf-8') as f:
        block_idx = 1
        for i in range(0, len(words), words_per_block):
            chunk = words[i:i+words_per_block]
            text_block = " ".join([w["text"] for w in chunk])
            start_time = format_srt_time(chunk[0]["start"])
            end_time = format_srt_time(chunk[-1]["end"])
            
            f.write(f"{block_idx}\n{start_time} --> {end_time}\n{text_block}\n\n")
            block_idx += 1

if __name__ == "__main__":
    # Définition des chemins (Modifie le nom du fichier JSON selon ton dernier export)
    dossier_prod = Path("C:/Users/pierr/dev/foliotype-protocol/cognition/output/mastered/production")
    
    # Recherche automatique du dernier fichier JSON de timestamps généré dans le dossier
    fichiers_json = sorted(dossier_prod.glob("*_timestamps.json"))
    
    if fichiers_json:
        dernier_json = fichiers_json[-1]
        fichier_srt_sortie = dernier_json.parent / dernier_json.name.replace("_timestamps.json", ".srt")
        
        print(f"🔄 Conversion de : {dernier_json.name}...")
        json_to_srt(dernier_json, fichier_srt_sortie, words_per_block=4)
        print(f"✅ Fichier .srt conforme généré : {fichier_srt_sortie.resolve()}")
    else:
        print("❌ Aucun fichier _timestamps.json trouvé dans le dossier de production.")