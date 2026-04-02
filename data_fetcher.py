import yfinance as yf
from GoogleNews import GoogleNews

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    # On récupère 1 mois d'historique pour le graphique
    hist = stock.history(period="1mo")
    
    if hist.empty:
        raise ValueError(f"Impossible de récupérer les données pour le ticker {ticker}.")

    current_price = round(hist['Close'].iloc[-1], 2)
    # Récupération du prix il y a 5 jours (ou le plus ancien disponible si moins de 5 jours)
    price_5d_ago = hist['Close'].iloc[-5] if len(hist) >= 5 else hist['Close'].iloc[0]
    variation = round(((current_price - price_5d_ago) / price_5d_ago) * 100, 2)

    return {
        "current_price": current_price,
        "variation_5d_pct": variation,
        "history": hist['Close'] # Données brutes pour le graphique Streamlit
    }

def get_stock_news(ticker):
    googlenews = GoogleNews(lang='fr', period='7d')
    googlenews.clear() 
    googlenews.search(f"{ticker} action bourse")
    
    results = googlenews.results()
    
    unique_titles = []
    titres_vus = set() # Un "set" permet de vérifier ultra-rapidement les doublons
    
    if results:
        # On boucle sur plus de résultats (20) pour être sûr d'en avoir 10 différents à la fin
        for res in results[:20]:
            titre = res.get('title')
            # Si le titre est valide ET qu'on ne l'a pas encore vu
            if titre and isinstance(titre, str) and titre not in titres_vus:
                titres_vus.add(titre)
                unique_titles.append(titre)
                
    # On ne garde que les 10 premiers titres uniques
    unique_titles = unique_titles[:10]
    
    if not unique_titles:
        unique_titles = ["Aucune actualité pertinente trouvée récemment."]
        
    news_text = "\n".join(unique_titles)
    
    return news_text, unique_titles