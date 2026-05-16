import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

FICHIER_COFFRE = "coffre.enc"
FICHIER_SALT = "coffre.salt"

def generer_cle(mot_de_passe_maitre: str, sel: bytes) -> bytes:
    """Dérive une clé de chiffrement à partir du mot de passe maître."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sel,
        iterations=600_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(mot_de_passe_maitre.encode()))

def charger_coffre(mot_de_passe_maitre: str) -> dict:
    """Déchiffre et charge le contenu du coffre-fort."""
    if not os.path.exists(FICHIER_COFFRE):
        return {}
        
    with open(FICHIER_COFFRE, "rb") as fichier:
        contents = fichier.read()
    
    try:
        with open(FICHIER_SALT, "rb") as f_salt:
            sel = f_salt.read()
    except FileNotFoundError:
        return {}

    cle = generer_cle(mot_de_passe_maitre, sel)
    f = Fernet(cle)
    try:
        donnees_dechiffrees = f.decrypt(contents)
        return json.loads(donnees_dechiffrees.decode())
    except Exception:
        raise ValueError("Mot de passe maître incorrect ou fichier corrompu.")

def sauvegarder_coffre(mot_de_passe_maitre: str, service: str, identifiant: str, mdp: str):
    """Ajoute ou met à jour un identifiant dans le coffre."""
    if not os.path.exists(FICHIER_SALT):
        sel = os.urandom(16)
        with open(FICHIER_SALT, "wb") as f_salt:
            f_salt.write(sel)
    else:
        with open(FICHIER_SALT, "rb") as f_salt:
            sel = f_salt.read()

    try:
        base = charger_coffre(mot_de_passe_maitre)
    except ValueError:
        base = {}

    base[service] = {"user": identifiant, "password": mdp}
    
    cle = generer_cle(mot_de_passe_maitre, sel)
    f = Fernet(cle)
    contenu_chiffre = f.encrypt(json.dumps(base).encode())
    
    with open(FICHIER_COFFRE, "wb") as fichier:
        fichier.write(contenu_chiffre)

def modifier_mot_de_passe(mot_de_passe_maitre: str, service: str, nouvel_identifiant: str, nouveau_mdp: str):
    """Modifie les identifiants d'un service existant."""
    base = charger_coffre(mot_de_passe_maitre)
    if service in base:
        base[service] = {"user": nouvel_identifiant, "password": nouveau_mdp}
        with open(FICHIER_SALT, "rb") as f_salt:
            sel = f_salt.read()
        cle = generer_cle(mot_de_passe_maitre, sel)
        f = Fernet(cle)
        contenu_chiffre = f.encrypt(json.dumps(base).encode())
        with open(FICHIER_COFFRE, "wb") as fichier:
            fichier.write(contenu_chiffre)
        print(f"[+] '{service}' a été modifié.")
    else:
        print(f"[!] Le service '{service}' n'existe pas dans le coffre.")

def supprimer_mot_de_passe(mot_de_passe_maitre: str, service: str):
    """Supprime définitivement un service du coffre-fort."""
    base = charger_coffre(mot_de_passe_maitre)
    if service in base:
        del base[service]
        with open(FICHIER_SALT, "rb") as f_salt:
            sel = f_salt.read()
        cle = generer_cle(mot_de_passe_maitre, sel)
        f = Fernet(cle)
        contenu_chiffre = f.encrypt(json.dumps(base).encode())
        with open(FICHIER_COFFRE, "wb") as fichier:
            fichier.write(contenu_chiffre)
        print(f"[-] '{service}' a été supprimé.")
    else:
        print(f"[!] Le service '{service}' n'existe pas dans le coffre.")

if __name__ == "__main__":
    try:
        with open("master.txt", "r", encoding="utf-8") as f_master:
            mdp_maitre = f_master.read().strip()
    except FileNotFoundError:
        print("[!] Erreur : Le fichier 'master.txt' est introuvable.")
        exit(1)

    print("--- MENU DU COFFRE-FORT ---")
    print("[a] Ajouter / Saisie continue")
    print("[v] Voir tous les mots de passe (Ordre alphabétique)")
    print("[m] Modifier un service")
    print("[s] Supprimer un service")
    choix = input("Votre choix : ").strip().lower()

    if choix == 'v':
        try:
            donnees = charger_coffre(mdp_maitre)
            # Tri des clés du dictionnaire par ordre alphabétique
            donnees_triees = {k: donnees[k] for k in sorted(donnees.keys())}
            print("\n--- CONTENU TRIÉ ---")
            print(json.dumps(donnees_triees, indent=4))
        except ValueError as e:
            print(f"[!] {e}")

    elif choix == 'm':
        service = input("Nom du service à modifier : ").strip()
        nouvel_user = input("Nouvel utilisateur : ")
        nouveau_mdp = input("Nouveau mot de passe : ")
        modifier_mot_de_passe(mdp_maitre, service, nouvel_user, nouveau_mdp)

    elif choix == 's':
        service = input("Nom du service à supprimer : ").strip()
        confirmation = input(f"Confirmer la suppression de {service} ? (oui/non) : ")
        if confirmation.lower() == 'oui':
            supprimer_mot_de_passe(mdp_maitre, service)

    elif choix == 'a':
        print("\n--- SAISIE CONTINUE ---")
        while True:
            service = input("Nom du service (ex: github) : ").strip()
            if not service:
                break
            identifiant = input("Nom d'utilisateur : ")
            mot_de_passe = input(f"Mot de passe pour {service} : ")
            sauvegarder_coffre(mdp_maitre, service, identifiant, mot_de_passe)
            print(f"[+] '{service}' ajouté.\n")