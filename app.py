import streamlit as st
import os
import main
import trading_executor

st.set_page_config(page_title="IA Trading Bot", page_icon="🤖", layout="centered")

st.title("📈 Comité d'Investissement IA")
st.markdown("*Une équipe d'agents IA autonomes qui analysent le marché à votre place.*")
st.markdown("---")

# ==========================================
# BARRE LATÉRALE COMPACTE
# ==========================================
st.sidebar.markdown("**🎯 1. Cible**")
ticker = st.sidebar.text_input("Symbole", value="MSFT", label_visibility="collapsed", placeholder="Ex: NVDA, MSFT...").upper()
quantite = st.sidebar.number_input("Quantité", min_value=1, value=1)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("**🧠 2. Moteur IA (Requis)**")
custom_gemini = st.sidebar.text_input("Clé Gemini", type="password", placeholder="Collez votre clé ici")
st.sidebar.caption("[Obtenir une clé gratuite](https://aistudio.google.com/app/apikey)")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("**🏦 3. Exécution**")
mode_demo = st.sidebar.toggle("Mode Démo (Sécurisé)", value=True)

custom_alpaca_key = ""
custom_alpaca_secret = ""

if not mode_demo:
    custom_alpaca_key = st.sidebar.text_input("Alpaca Key ID", type="password", placeholder="Key ID")
    custom_alpaca_secret = st.sidebar.text_input("Alpaca Secret", type="password", placeholder="Secret Key")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
lancer = st.sidebar.button("🚀 Lancer l'Analyse", use_container_width=True, type="primary")

# ==========================================
# LOGIQUE PRINCIPALE
# ==========================================
if lancer:
    if not custom_gemini:
        st.error("⚠️ Veuillez entrer une clé API Gemini pour lancer l'analyse.")
    else:
        try:
            with st.spinner('🔍 Les IA analysent la situation avec une précision algorithmique...'):
                
                # Exécution du script principal
                rapport_s, rapport_q, decision, hist_data, sources = main.run_trading_bot(ticker, user_gemini_key=custom_gemini)
                
                # --- AFFICHAGE DU GRAPHIQUE ---
                st.subheader(f"📊 Évolution du cours : {ticker} (30 derniers jours)")
                st.line_chart(hist_data)
                
                # --- RAPPORTS & SOURCES ---
                with st.expander("🗣️ Rapport de l'Analyste Sentiment"):
                    st.write(rapport_s)
                    st.markdown("---")
                    st.markdown("**📰 Sources lues par l'IA :**")
                    for title in sources:
                        st.caption(f"- {title}")
                    
                with st.expander("📊 Rapport de l'Analyste Quantitatif"):
                    st.write(rapport_q)
                    
                st.markdown("---")
                
                # --- VERDICT FINAL ---
                st.subheader("🎯 Verdict du Boss")
                premier_mot = decision.strip().upper().replace(".", " ").replace(",", " ").split()[0]
                
                if "ACHETER" in premier_mot:
                    st.success(f"### ✅ DÉCISION : ACHETER\n{decision[7:]}") 
                elif "VENDRE" in premier_mot:
                    st.error(f"### 🚨 DÉCISION : VENDRE\n{decision[6:]}")
                elif "ATTENDRE" in premier_mot:
                    st.info(f"### ⏳ DÉCISION : ATTENDRE\n{decision[8:]}")
                else:
                    st.warning(f"🤔 {decision}")

                st.markdown("---")
                
                # --- EXÉCUTION ALPACA ---
                if mode_demo:
                    if premier_mot in ["ACHETER", "VENDRE"]:
                        st.success(f"Simulation : Un ordre de {premier_mot} pour {quantite} action(s) {ticker} aurait été exécuté.")
                    else:
                        st.info("Simulation : Le marché est en attente, aucune action effectuée.")
                else:
                    if custom_alpaca_key and custom_alpaca_secret:
                        os.environ["ALPACA_API_KEY"] = custom_alpaca_key
                        os.environ["ALPACA_SECRET_KEY"] = custom_alpaca_secret
                        
                        with st.spinner("Transmission au courtier..."):
                            trading_executor.executer_ordre(decision, ticker=ticker, quantite=quantite)
                            st.success("Ordre réel transmis à Alpaca avec succès !")
                    else:
                        st.error("⚠️ Veuillez fournir vos clés Alpaca.")

        except Exception as e:
            st.error(f"⚠️ Erreur lors de l'analyse : {e}")

# ==========================================
# EXEMPLE VISUEL (SI NON LANCÉ)
# ==========================================
else:
    st.info("👈 Paramétrez l'analyse à gauche et ajoutez votre clé Gemini pour commencer. \n\n*Vous n'avez pas de clé sous la main ? Regardez l'exemple ci-dessous.*")
    st.markdown("---")
    st.markdown("### 👀 Exemple d'analyse (NVIDIA - NVDA)")
    
    # --- NOUVEAU : Le faux graphique statique ---
    st.subheader("📊 Évolution du cours : NVDA (30 derniers jours)")
    # Une liste de prix fictifs montrant une belle tendance haussière
    donnees_nvda_exemple = [112.5, 114.0, 113.2, 115.8, 118.1, 117.5, 119.2, 121.0, 120.5, 122.8, 124.5, 123.9, 125.1, 127.4, 126.8, 128.5, 130.2, 129.5, 131.0, 132.5]
    st.line_chart(donnees_nvda_exemple)
    
    with st.expander("🗣️ Rapport de l'Analyste Sentiment (Exemple)"):
        st.write("L'analyse exclusive des actualités concernant NVIDIA révèle un consensus extrêmement haussier. Les annonces récentes autour de l'architecture Blackwell et la demande pour les puces d'IA générative dominent la presse financière. Les craintes liées à la valorisation sont largement éclipsées par les révisions à la hausse des objectifs de cours par les analystes majeurs.\n\n**Note de Sentiment : 8.5/10**")
        st.markdown("---")
        st.markdown("**📰 Sources lues par l'IA :**")
        st.caption("- NVIDIA pulvérise les attentes de Wall Street pour le trimestre")
        st.caption("- La demande pour les puces Blackwell est 'sans précédent' selon le PDG")
        st.caption("- Morgan Stanley relève son objectif de cours sur l'action NVDA")
        st.caption("- Pourquoi l'action NVIDIA reste le leader incontesté de l'IA")
        
    with st.expander("📊 Rapport de l'Analyste Quantitatif (Exemple)"):
        st.write("Prix actuel: 132.50$. Tendance 5 jours: +4.2%.\n\nLa dynamique mathématique à court terme est nettement favorable. Le titre affiche une progression constante avec des creux de plus en plus hauts, confirmant une impulsion directionnelle haussière robuste. L'absence de divergence négative suggère que l'élan acheteur reste dominant à ce stade.")
        
    st.success("""### ✅ DÉCISION : ACHETER\n**Conviction : 85%**\n\nL'alignement est optimal entre des catalyseurs fondamentaux puissants (Note 8.5/10) et une configuration technique résolument haussière (+4.2% sur 5 jours). Les indicateurs exigent une prise de position à l'achat pour capter la poursuite de cette dynamique de marché.""")
    st.caption("🏦 *Simulation : Un ordre de ACHETER pour 1 action(s) NVDA aurait été exécuté avec succès.*")
# ==========================================
# FOOTER ET AVERTISSEMENT LÉGAL
# ==========================================
st.markdown("---")
col_texte, col_signature = st.columns([3, 1])
with col_texte:
    st.warning("""
    **⚠️ Avertissement Légal & Décharge de Responsabilité** 
               
    Ce tableau de bord est un projet personnel et une démonstration technique à but strictement éducatif. **Je ne suis pas un conseiller financier.** 
               
    Les analyses, scores et décisions générés par les modèles d'Intelligence Artificielle ne constituent en aucun cas des conseils d'investissement. 
               L'utilisation de cet outil se fait à vos propres risques. 
               
    L'auteur décline toute responsabilité quant aux éventuelles pertes financières liées à l'utilisation de cet outil.
    """)
with col_signature:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("👨‍💻 **Par Julien DUBUC**")
    st.caption("Projet IA & Finance - 2026")

    # --- NOUVEAU : Les liens avec logos (Badges) ---
    # N'oublie pas de remplacer les URL entre parenthèses par tes vrais liens !
    st.markdown("""
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/julien-dubuc14/)
    
    [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/julien-dbc)
    
    [![Portfolio](https://img.shields.io/badge/Portfolio-255E63?style=flat&logo=googlechrome&logoColor=white)](https://julien-dbc.github.io/portfolio/)
    """)