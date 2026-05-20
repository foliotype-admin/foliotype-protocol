import requests

api_key = "VOTRE_CLE_API"
headers = {"xi-api-key": api_key}

# Récupération de toutes les voix
voices_req = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
voices_data = voices_req.json()

# Suppression de chaque voix trouvée pour réinitialiser les slots
if voices_data.get('voices'):
    for v in voices_data['voices']:
        voice_id = v['voice_id']
        name = v['name']
        print(f"Tentative de suppression de : {name} ({voice_id})...")
        del_req = requests.delete(f"https://api.elevenlabs.io/v1/voices/{voice_id}", headers=headers)
        print(f"Statut : {del_req.status_code}")
else:
    print("Aucune voix à supprimer.")