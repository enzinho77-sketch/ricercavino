import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

st.set_page_config(page_title="VinoFinder 2.0", layout="wide")

st.title("🍷 Ricerca Vino 2.0 - Filtro Automatico")
st.markdown("L'app mostra i link **solo se il vino viene trovato** sull'e-commerce.")

shops = {
    "Tannico": "tannico.it",
    "Bernabei": "bernabei.it",
    "Vino.com": "vino.com",
    "Callmewine": "callmewine.com"
}

def verifica_presenza(site, vino):
    """Verifica se il vino esiste sul sito usando Google senza farsi bloccare."""
    query = f"site:{site} {vino}"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Se Google dice che non ci sono risultati per la ricerca 'site:...'
        if "non ha prodotto risultati" in response.text or "did not match any documents" in response.text:
            return None
        return url
    except:
        return None

# --- INPUT ---
col1, col2 = st.columns(2)
with col1:
    manual_wine = st.text_input("Inserisci etichetta")
with col2:
    uploaded_file = st.file_uploader("Carica Excel", type=['xlsx'])

vini = []
if manual_wine: vini.append(manual_wine)
if uploaded_file:
    # Soluzione per leggere TUTTE le schede (fogli) dell'Excel
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    for sheet_name, df in all_sheets.items():
        vini.extend(df.iloc[:, 0].dropna().tolist())

if vini:
    st.divider()
    st.write(f"🔍 Analisi in corso per {len(vini)} etichette... Attendere.")
    
    cols = st.columns(len(shops))
    for idx, (shop_name, domain) in enumerate(shops.items()):
        with cols[idx]:
            st.subheader(shop_name)
            for v in vini:
                link_valido = verifica_presenza(domain, v)
                if link_valido:
                    st.success(f"🔗 [{v}]({link_valido})")
                # Se non è valido, non scrive nulla (come richiesto)
                time.sleep(0.5) # Pausa per non farci bloccare da Google
