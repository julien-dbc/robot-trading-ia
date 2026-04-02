# 📈 Comité d'Investissement IA (Trading Bot)

Une application web interactive qui orchestre plusieurs agents d'Intelligence Artificielle pour analyser le marché financier et simuler des prises de décision de trading.

L'objectif de ce projet est de démontrer l'intégration de LLMs dans un flux de travail décisionnel complexe (analyse de sentiment + analyse quantitative), le tout packagé dans une interface utilisateur intuitive.

## ✨ Fonctionnalités

* **Orchestration Multi-Agents** : Utilisation de l'API Google Gemini pour faire interagir 3 "personnas" distincts (Analyste Sentiment, Analyste Quantitatif, Gestionnaire de Portefeuille).
* **Données en Temps Réel** : Récupération de l'historique des prix via `yfinance` et du flux d'actualités via `GoogleNews`.
* **Interface Web Interactive** : Développée avec Streamlit, permettant aux utilisateurs d'entrer leurs propres clés API (Bring Your Own Key) pour tester sans risque de quotas.
* **Mode Démo Sécurisé** : Un système de Paper Trading intégré avec l'API Alpaca, désactivable pour la démonstration publique.
* **Déterministe** : Température des LLMs fixée à 0 pour garantir des résultats analytiques constants.

## 🛠️ Architecture Technique

1.  **Data Fetching** : Scrape les 10 derniers articles de presse uniques et l'historique des prix sur 30 jours.
2.  **Agent Sentiment** : LLM bridé pour extraire uniquement le sentiment lié au ticker cible et générer un score sur 10.
3.  **Agent Quantitatif** : LLM chargé d'analyser la dynamique mathématique des prix.
4.  **Meta-Agent (Le Boss)** : Synthétise les deux rapports précédents pour générer une décision finale (ACHETER, VENDRE, ATTENDRE) avec un niveau de conviction en %.