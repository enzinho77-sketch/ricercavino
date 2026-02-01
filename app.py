import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

st.set_page_config(page_title="VinoFinder 2.0", layout="wide")

st.title("🍷 Ricerca Vino 2.0 - Filtro Intelligente")
st.markdown("L'app verifica l'effettiva presenza dell'etichetta e mostra il link **solo se disponibile**.")

shops = {
    "Tannico": "tannico.it",
    "Bernabei": "bernabei.it",
    "Vino.com": "vino.com",
    "Callmewine": "callmewine.com"
}

def controlla_esistenza_reale(site, vino):
    """Controlla se Google trova effettivamente il vino su quel dominio."""
    query = f'site:{site} "{vino}"' # Le virgolette forzano la ricerca esatta
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Se nella pagina appare la frase tipica di 'nessun risultato'
        testo_errore = ["non ha prodotto risultati", "did not match any documents", "Suggerimenti:"]
        if any(x in response.text for x in testo_errore) and "Risultati per" not in response.text:
            return None
        return url
    except:
        return None

# --- CARICAMENTO DATI ---
uploaded_file = st.file_uploader("Carica Excel con più schede", type=['xlsx'])
manual_wine = st.text_input("Oppure scrivi qui un'etichetta singola")

vini_finali = []

if uploaded_file:
    # Legge TUTTI i fogli del file Excel
    dizionario_fogli = pd.read_excel(uploaded_file, sheet_name=None)
    for nome_foglio, df in dizionario_fogli.items():
        if not df.empty:
            # Prende la prima colonna di ogni foglio
            vini_finali.extend(df.iloc[:, 0].dropna().astype(str).tolist())

if manual_wine:
    vini_finali.append(manual_wine)

# --- ESECUZIONE RICERCA ---
if vini_finali:
    vini_unici = list(dict.fromkeys(vini_finali)) # Rimuove duplicati
    st.info(f"Analisi di {len(vini_unici)} etichette in corso... L'operazione richiede qualche secondo per evitare blocchi.")
    
    colonne_shop = st.columns(len(shops))
    
    for i, (nome_shop, dominio) in enumerate(shops.items()):
        with colonne_shop[i]:
            st.header(nome_shop)
            for v in vini_unici:
                with st.spinner(f'Verifico {v}...'):
                    link = controlla_esistenza_reale(dominio, v)
                    if link:
                        st.success(f"🍷 [{v}]({link})")
                    # Piccola pausa per non essere scambiati per bot da Google
                    time.sleep(1)
