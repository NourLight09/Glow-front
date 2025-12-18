import streamlit as st
import textwrap
import time
import datetime
import re

# Base de données Produits Simulée (Catalogue GLOW)
MOCK_PRODUCTS = {
    "nettoyant": {
        "grasse": {"name": "Purifying Gel Cleanser", "price": "24€", "ing": "Zinc, Acide Salicylique", "desc": "Gel moussant purifiant intense."},
        "seche": {"name": "Milky Oil Cleanser", "price": "28€", "ing": "Huile d'Amande, Céramides", "desc": "Lait-huile reconfortant."},
        "normale": {"name": "Gentle Foam", "price": "22€", "ing": "Eau de Rose, Aloe Vera", "desc": "Mousse aérienne douce."},
        "sensible": {"name": "Calming Balm", "price": "30€", "ing": "Centella Asiatica, Avoine", "desc": "Baume fondant apaisant."}
    },
    "serum": {
        "eclat": {"name": "Vitamin C Radiance", "price": "45€", "ing": "Vitamine C 15%, Ferulic Acid", "desc": "Boost d'éclat immédiat."},
        "rides": {"name": "Retinol Renew", "price": "55€", "ing": "Retinol 0.3%, Peptides", "desc": "Lisse et raffermit la peau."},
        "imperfections": {"name": "Niacinamide Zinc", "price": "35€", "ing": "Niacinamide 10%, Zinc 1%", "desc": "Réduit les pores et imperfections."},
        "deshydratation": {"name": "Hyaluronic Boost", "price": "42€", "ing": "Acide Hyaluronique Multi-PM", "desc": "Hydratation profonde par couches."}
    },
    "creme": {
        "riche": {"name": "Deep Repair Cream", "price": "48€", "ing": "Beurre de Karité, Squalane", "desc": "Nutrition intense nuit."},
        "legere": {"name": "Hydro-Gel Cloud", "price": "38€", "ing": "Eau de Glacier, Concombre", "desc": "Gelée hydratante fini mat."},
        "active": {"name": "Pro-Collagen Cream", "price": "65€", "ing": "Collagène Marin, Algues", "desc": "Fermeté et rebond."}
    }
}

def show_home(navigate_callback):
    st.markdown("<h1 style='text-align: center; font-size: 6rem; font-family: Playfair Display, serif; margin-top: 50px;'>GLOW</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 50px;'>VOTRE CONSULTANT BEAUTÉ INTELLIGENT</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("LANCER LE DIAGNOSTIC"):
            navigate_callback('diagnosis')

def derive_skin_profile(data):
    # Logique simple pour déterminer le type de peau pour l'affichage
    oil = data.get('oil', 5)
    hydration = data.get('hydration', 5)
    sens = data.get('sensitivity', 3)
    
    skin_type = "NORMALE"
    concern = "ÉCLAT"
    
    if sens > 6:
        skin_type = "SENSIBLE"
        concern = "APAISANTE"
    elif oil > 7:
        skin_type = "GRASSE"
        concern = "MATIFIANT"
    elif oil < 3:
        skin_type = "SÈCHE"
        concern = "NUTRITION"
    elif oil > 6 and hydration < 4:
        skin_type = "MIXTE DÉSHYDRATÉE"
        concern = "RÉÉQUILIBRANTE"
    elif hydration < 3:
        skin_type = "DÉSHYDRATÉE"
        concern = "HYDRATATION INTENSE"
        
    return skin_type, concern

def get_product_selection(skin_type, concern):
    # Logique de sélection simple
    # 1. Nettoyant selon Type de Peau
    if "GRASSE" in skin_type: cle_type = "grasse"
    elif "SÈCHE" in skin_type or "DÉSHYDRATÉE" in skin_type: cle_type = "seche"
    elif "SENSIBLE" in skin_type: cle_type = "sensible"
    else: cle_type = "normale"
    
    # 2. Sérum selon Préoccupation
    if "RIDE" in concern.upper(): ser_type = "rides"
    elif "ACNÉ" in concern.upper() or "MATIFIANT" in concern.upper(): ser_type = "imperfections"
    elif "DÉSHYDRATÉE" in skin_type: ser_type = "deshydratation"
    else: ser_type = "eclat" # Default
    
    # 3. Crème selon Type
    if "SÈCHE" in skin_type: cre_type = "riche"
    elif "GRASSE" in skin_type: cre_type = "legere"
    else: cre_type = "active"
    
    return [
        MOCK_PRODUCTS["nettoyant"].get(cle_type, MOCK_PRODUCTS["nettoyant"]["normale"]),
        MOCK_PRODUCTS["serum"].get(ser_type, MOCK_PRODUCTS["serum"]["eclat"]),
        MOCK_PRODUCTS["creme"].get(cre_type, MOCK_PRODUCTS["creme"]["active"])
    ]

def show_diagnosis(navigate_callback):
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Diagnostiquez votre Peau</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    diagnosis_html = textwrap.dedent("""
    <div style='background-color: #ffdce5; padding: 20px; border-radius: 5px; margin-bottom: 30px; border-left: 3px solid #5e1223; color: #5e1223;'>
        <p style='margin:0; font-style:italic; color: #5e1223;'>Pour établir votre profil dermo-cosmétique précis, veuillez renseigner vos indicateurs biologiques. Nos algorithmes calculeront votre typologie exacte.</p>
    </div>
    """)
    st.markdown(diagnosis_html.strip(), unsafe_allow_html=True)
    
    with st.form("diagnosis_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Prénom")
            age = st.number_input("Âge", min_value=16, max_value=90, value=25)
        with c2:
            gender = st.selectbox("Genre", ["Femme", "Homme", "Autre"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Indicateurs Biologiques")
        
        hydration = st.slider("Niveau d'Hydratation", 0, 10, 5, help="0=Peau qui tire très fort, 10=Peau très rebondie", key="hydration")
        st.caption("0 : Très sèche (Tiraillements) — 10 : Très hydratée (Souple)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        oil_level = st.slider("Niveau de Sébum (Gras)", 0, 10, 5, key="oil")
        st.caption("0 : Mate/Sèche — 10 : Très brillante/Grasse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        sensitivity = st.slider("Niveau de Sensibilité", 0, 10, 3, key="sens")
        st.caption("0 : Peau résistante — 10 : Rougeurs et réactions fréquentes")
        
        st.markdown("<br>", unsafe_allow_html=True)

        budget = st.select_slider("Budget Soins (Mensuel)", options=["€ Eco", "€€ Standard", "€€€ Premium"], value="€€ Standard", key="budget")
        st.caption("Ajuste la sélection de produits selon votre investissement souhaité.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("GÉNÉRER MON ÉDITION SPÉCIALE")
        
        if submitted:
            if name:
                # Sauvegarde des données
                st.session_state.user_data = {
                    'name': name,
                    'age': age,
                    'gender': gender,
                    'hydration': hydration,
                    'oil': oil_level,
                    'sensitivity': sensitivity,
                    'budget': budget
                }
                
                with st.spinner('Analyse des biomarqueurs en cours...'):
                    time.sleep(1.5)
                    navigate_callback('magazine')
            else:
                st.error("Merci d'indiquer votre prénom pour la couverture du magazine.")

def show_magazine(navigate_callback):
    user = st.session_state.user_data
    name = user.get('name', 'Chère Lectrice')
    age = user.get('age', 25)
    
    skin_type, concern = derive_skin_profile(user)
    products = get_product_selection(skin_type, concern)
    
    today = datetime.date.today().strftime("%B %Y")
    
    # Injection HTML pour la mise en page Magazine
    magazine_html = f"""
    <div class="magazine-container">
        <!-- EN-TÊTE COUVERTURE -->
        <div class="cover-header">
            <h1 class="brand-title">GLOW</h1>
            <div class="issue-details">
                <span>ÉDITION SPÉCIALE &bull; {age} ANS</span>
                <span>{today}</span>
                <span>VOL. 1</span>
            </div>
        </div>
        
        <!-- IMAGE HÉRO -->
        <div class="cover-hero">
            <img src="https://images.unsplash.com/photo-1596462502278-27bfdd403348?q=80&w=1000&auto=format&fit=crop">
        </div>
        
        <!-- GROS TITRES -->
        <div class="headline-overlay">
            <div class="sub-headline">L'INTELLIGENCE ARTIFICIELLE RÉVÈLE</div>
            <div class="main-headline">VOTRE ROUTINE IDEALE<br>POUR PEAU {skin_type}</div>
            <div style="width: 50px; height: 1px; background: #5e1223; margin: 20px auto;"></div>
            <p style="font-style: italic;">Objectif : {concern}</p>
        </div>
        
        <!-- ÉDITO -->
        <div class="editorial-section">
            <h2 style="text-align: center; margin-bottom: 30px; font-size: 2rem;">LE MOT DE L'EXPERT</h2>
            <div class="editorial-layout">
                <p><span class="drop-cap">B</span>onjour {name},</p>
                <p>À {age} ans, votre peau a des besoins précis. Notre analyse montre que vous avez une peau <strong>{skin_type.lower()}</strong>.</p>
                <p>Ce que cela signifie : votre peau a besoin d'aide pour gérer son équilibre. Votre priorité est de traiter <strong>{concern.lower()}</strong>.</p>
                <p>Nous avons sélectionné pour vous 3 produits d'exception. Voici votre routine détaillée.</p>
                <p style="text-align: right; margin-top: 20px; font-weight: bold;">— Votre Coach Beauté</p>
            </div>
        </div>
        
        <!-- TIMELINE ROUTINE (NOUVEAU DESIGN) -->
        <div class="timeline-section">
            <h2 style="text-align:center; color: #5e1223; margin-bottom: 50px;">VOTRE AGENDA BEAUTÉ</h2>
            
            <div class="timeline-item">
                <div class="timeline-time">08:00</div>
                <div class="timeline-content">
                    <h3 class="timeline-title">Le Réveil Éclat</h3>
                    <p>Nettoyez votre visage avec <strong>{products[0]['name']}</strong> pour éliminer les impuretés de la nuit. Une base saine est essentielle.</p>
                </div>
            </div>
            
            <div class="timeline-item">
                <div class="timeline-time">08:15</div>
                <div class="timeline-content">
                    <h3 class="timeline-title">L'Hydratation</h3>
                    <p>Appliquez le sérum <strong>{products[1]['name']}</strong> puis scellez l'hydratation. N'oubliez pas votre SPF !</p>
                </div>
            </div>
            
            <div class="timeline-item">
                <div class="timeline-time">22:00</div>
                <div class="timeline-content">
                    <h3 class="timeline-title">Le Soir Régénérant</h3>
                    <p>Le moment clé. Utilisez <strong>{products[2]['name']}</strong> pour réparer votre peau durant le sommeil.</p>
                </div>
            </div>
        </div>

        <!-- SÉLECTION PRODUITS DÉTAILLÉE -->
        <div class="product-grid">
            <div style="grid-column: 1 / -1; text-align: center; margin-bottom: 20px;">
                <h2>VOTRE SÉLECTION PERSONNALISÉE</h2>
                <p>LES PRODUITS DE VOTRE ROUTINE</p>
            </div>
            
            <!-- PRODUIT 1 -->
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400">
                <div class="product-name">{products[0]['name']}</div>
                <div class="product-price">{products[0]['price']}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #888; margin-bottom: 10px;">{products[0]['ing']}</div>
                <div class="product-desc">{products[0]['desc']}</div>
            </div>

            <!-- PRODUIT 2 -->
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1608248597279-f99d160bfbc8?w=400">
                <div class="product-name">{products[1]['name']}</div>
                <div class="product-price">{products[1]['price']}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #888; margin-bottom: 10px;">{products[1]['ing']}</div>
                <div class="product-desc">{products[1]['desc']}</div>
            </div>

            <!-- PRODUIT 3 -->
            <div class="product-card">
                <img src="https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=400">
                <div class="product-name">{products[2]['name']}</div>
                <div class="product-price">{products[2]['price']}</div>
                <div style="font-size: 0.8rem; font-style: italic; color: #888; margin-bottom: 10px;">{products[2]['ing']}</div>
                <div class="product-desc">{products[2]['desc']}</div>
            </div>
            
        </div>
        
    </div>
    """
    
    # Nettoyage de l'indentation pour éviter les conflits Markdown
    magazine_html = re.sub(r'^\s+', '', magazine_html, flags=re.MULTILINE)
    st.markdown(magazine_html, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("TÉLÉCHARGER (PDF)"):
            st.toast("Votre magazine est en cours de téléchargement...")
    with col2:
        if st.button("NOUVEAU DIAGNOSTIC"):
            navigate_callback('home')
