import streamlit as st
import pandas as pd
import requests
import urllib.parse
import time

st.set_page_config(page_title="VinoFinder Pro", layout="wide")

st.title("🍷 VinoFinder Pro - Filtro Reale")
st.markdown("Verifica la disponibilità reale direttamente sugli e-commerce.")

# Configurazione parametri di ricerca
SHOPS = {
    "Tannico": {"url": "https://www.tannico.it/catalogsearch/result/?q=", "not_found": "non ha prodotto risultati"},
    "Bernabei": {"url": "https://www.bernabei.it/catalogsearch/result/?q=", "not_found": "nessun risultato"},
    "Vino.com": {"url": "https://www.vino.com/search?q=", "not_found": "non abbiamo trovato"},
    "Callmewine": {"url": "https://www.callmewine.com/catalogsearch/result/?q=", "not_found": "non ha prodotto risultati"}
}

def verifica_disponibilita_diretta(shop_name, vino):
    """Interroga direttamente il sito e capisce se il prodotto esiste."""
    base_url = SHOPS[shop_name]["url"]
    search_url = f"{base_url}{urllib.parse.quote(str(vino))}"
    
    # Header per sembrare un browser vero
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'it-IT,it;q=0.9'
    }
    
    try:
        # Usiamo una sessione per gestire meglio le connessioni
        session = requests.Session()
        response = session.get(search_url, headers=headers, timeout=10)
        
        # Se il sito risponde correttamente (200) e NON contiene la frase "non trovato"
        testo_errore = SHOPS[shop_name]["not_found"]
        if response.status_code == 200 and testo_errore not in response.text.lower():
            return search_url
        return None
    except:
        return None

# --- CARICAMENTO ---
uploaded_file = st.file_uploader("Carica Excel (legge tutte le schede)", type=['xlsx'])
manual_wine = st.text_input("Inserimento manuale")

vini_input = []
if uploaded_file:
    fogli = pd.read_excel(uploaded_file, sheet_name=None)
    for nome, df in fogli.items():
        if not df.empty:
            vini_input.extend(df.iloc[:, 0].dropna().astype(str).tolist())
if manual_wine:
    vini_input.append(manual_wine)

# --- DISPLAY ---
if vini_input:
    vini_unici = list(dict.fromkeys(vini_input))
    st.info(f"Ricerca in corso su {len(vini_unici)} etichette...")
    
    # Creiamo una griglia
    cols = st.columns(len(SHOPS))
    
    for i, shop_name in enumerate(SHOPS.keys()):
        with cols[i]:
            st.header(shop_name)
            for v in vini_unici:
                with st.spinner(f'Checking {v}...'):
                    link_certo = verifica_disponibilita_diretta(shop_name, v)
                    if link_certo:
                        st.success(f"✔️ [{v}]({link_certo})")
                # Pausa minima anti-blocco
                time.sleep(0.2)
