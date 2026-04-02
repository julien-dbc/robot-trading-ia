import os
from google import genai
from google.genai import types 
from dotenv import load_dotenv
import data_fetcher
import trading_executor

load_dotenv()

def run_trading_bot(ticker="MSFT", user_gemini_key=None):
    # 1. Gestion de la clé API
    api_key = user_gemini_key if user_gemini_key else os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("⚠️ Aucune clé API Gemini n'a été trouvée.")

    client = genai.Client(api_key=api_key)

    # 2. Fonction utilitaire pour appeler les agents
    def call_agent(role, prompt, data):
        full_prompt = f"Tu es un {role}.\nDonnées : {data}\nTâche : {prompt}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=0.0, # Zéro hasard, réponses déterministes
            )
        )
        return response.text

    # 3. Récupération des données via data_fetcher
    print(f"🔄 Récupération des données pour {ticker}...")
    prix_data = data_fetcher.get_stock_data(ticker)
    news_text, news_titles = data_fetcher.get_stock_news(ticker)
    
    prix_texte = f"Prix actuel: {prix_data['current_price']}$. Tendance 5 jours: {prix_data['variation_5d_pct']}%."

    # --- Agent 1 : Sentiment ---
    rapport_sentiment = call_agent(
        role="Expert financier quantitatif de Wall Street",
        prompt=f"Rédige une analyse stricte et factuelle du sentiment des actualités EXCLUSIVEMENT pour l'action {ticker}. Ignore totalement les performances des entreprises concurrentes (comme NVIDIA, Apple, etc.) même si elles sont mentionnées dans le texte. Tu dois IMPÉRATIVEMENT répondre en FRANÇAIS. Termine par une 'Note de Sentiment : X/10'.",
        data=news_text
    )

    # --- Agent 2 : Quantitatif ---
    rapport_quantitatif = call_agent(
        role="Mathématicien froid et algorithmique",
        prompt="Analyse cette tendance de prix avec précision. Dis si la dynamique mathématique à court terme est favorable, neutre ou risquée. Tu dois IMPÉRATIVEMENT répondre en FRANÇAIS.",
        data=prix_texte
    )

    # --- Agent 3 : Gestionnaire ---
    rapport_combine = f"Rapport Sentiment :\n{rapport_sentiment}\n\nRapport Quantitatif :\n{rapport_quantitatif}"
    decision_finale = call_agent(
        role="Patron d'un fonds d'investissement algorithmique, extrêmement pragmatique",
        prompt="Lis ces rapports. Prends ta décision (ACHETER, VENDRE, ou ATTENDRE). Ta réponse DOIT commencer par un de ces trois mots en majuscules. Ensuite, va à la ligne et écris 'Conviction : X%' en justifiant factuellement ce pourcentage en 2 phrases en FRANÇAIS.",
        data=rapport_combine
    )
    
    # 4. On retourne tous les éléments à l'interface graphique
    return rapport_sentiment.strip(), rapport_quantitatif.strip(), decision_finale.strip(), prix_data['history'], news_titles

if __name__ == "__main__":
    # Test dans le terminal
    s, q, d, hist, sources = run_trading_bot("AAPL")
    print(d)