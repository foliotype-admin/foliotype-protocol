import re

def appliquer_protocole_foliotype(texte_source):
    # Intégration de votre variante compacte pour la désignation
    substitutions_validees = {
        r"\bHybrid Warfare Analytical Group\b": "Haïebrid Worfaire Analiticol Group",
        r"\bHWAG\b": "H-W-AG"
    }
    
    texte_traite = texte_source
    for motif, remplacement in substitutions_validees.items():
        texte_traite = re.sub(motif, remplacement, texte_traite)
        
    return texte_traite

phrase_test = "Il dirige le Hybrid Warfare Analytical Group (HWAG)."

print("=== SÉCURISATION DU FLUX TEXTUEL ===")
print(f"Entrée brute : {phrase_test}")
print(f"Sortie API   : {appliquer_protocole_foliotype(phrase_test)}")
print("====================================")