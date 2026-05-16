import time

# --- TECHNICAL CONFIGURATION ---
VERSION = "4.1.0"
BUILD_TAG = "FT2026-05-15-MASTER-S"  # Signature d'antériorité discrète
LOG_LEVEL = "INFO"

def run_process():
    print(f"--- FOLIOTYPE CORE v{VERSION} ---")
    print(f"Status: Operational")
    print(f"Build ID: {BUILD_TAG}")  # <--- C'est cette ligne qui génère l'affichage
    time.sleep(0.5)
    print("Process complete.")

if __name__ == "__main__":
    run_process()
