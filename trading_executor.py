import os
import requests
from dotenv import load_dotenv

# Chargement des clés
load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

def executer_ordre(decision_texte, ticker="MSFT", quantite=1):
    if not API_KEY or not SECRET_KEY:
        print("⚠️ Erreur : Clés Alpaca introuvables dans le fichier .env !")
        return

    print("\n🏦 --- CONNEXION À LA BOURSE (ALPACA) --- 🏦")

    # --- LE CORRECTIF EST ICI ---
    # On nettoie le texte, on le met en majuscule, on remplace la ponctuation par des espaces
    decision_propre = decision_texte.strip().upper().replace(".", " ").replace(",", " ")
    # On isole uniquement le tout premier mot du texte
    premier_mot = decision_propre.split()[0] if decision_propre else ""
    
    headers = {
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": SECRET_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}/v2/orders"

    try:
        # On vérifie uniquement le premier mot
        if premier_mot == "ACHETER":
            print(f"📈 Ordre d'ACHAT en cours pour {quantite} action(s) {ticker}...")
            data = {
                "symbol": ticker,
                "qty": quantite,
                "side": "buy",
                "type": "market",
                "time_in_force": "gtc"
            }
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                print("✅ SUCCÈS : Ordre d'achat exécuté virtuellement sur Alpaca !")
            else:
                print(f"❌ Refusé par Alpaca : {response.text}")
                
        elif premier_mot == "VENDRE":
            print(f"📉 Ordre de VENTE en cours pour {quantite} action(s) {ticker}...")
            data = {
                "symbol": ticker,
                "qty": quantite,
                "side": "sell",
                "type": "market",
                "time_in_force": "gtc"
            }
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                print("✅ SUCCÈS : Ordre de vente exécuté virtuellement sur Alpaca !")
            else:
                print(f"❌ Refusé par Alpaca : {response.text}")
                
        elif premier_mot == "ATTENDRE":
            print("⏳ Instruction reçue : ATTENDRE. Aucun ordre n'a été envoyé sur le marché.")
            
        else:
            print(f"🤔 Erreur : Le premier mot n'est pas reconnu ({premier_mot}). Texte : {decision_texte}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion réseau : {e}")