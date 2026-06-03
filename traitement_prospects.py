# traitement_prospects.py
import csv
import os

def charger_et_traiter_prospects(fichier_csv):
    if not os.path.exists(fichier_csv):
        print(f"Erreur : Le fichier {fichier_csv} n'existe pas.")
        return

    with open(fichier_csv, mode='r', encoding='utf-8') as f:
        # DictReader utilise la première ligne (headers) comme clés pour chaque ligne
        lecteur = csv.DictReader(f)
        
        for ligne in lecteur:
            # Traitement de la logique selon le statut
            if ligne['statut'] == 'a_contacter':
                print(f"--- Envoi de mail requis ---")
                print(f"À : {ligne['contact_nom']} ({ligne['nom_entreprise']})")
                print(f"Email : {ligne['email']}")
                print(f"Pitch utilisé : {ligne['pitch_personnalise']}\n")
            elif ligne['statut'] == 'en_cours':
                print(f"=> Prospect {ligne['nom_entreprise']} déjà contacté (En cours).\n")

if __name__ == "__main__":
    nom_fichier = "prospects.csv"
    charger_et_traiter_prospects(nom_fichier)