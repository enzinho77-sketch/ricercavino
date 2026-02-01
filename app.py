import streamlit as st
import pandas as pd
import urllib.parse

# Configurazione Pagina
st.set_page_config(page_title="VinoFinder Fast", layout="wide")

st.title("🍷 VinoFinder Fast - Zero Blocchi")
st.markdown("I siti bloccano i robot? Risolviamo aprendo le ricerche direttamente nel tuo browser.")

# Configurazione Link di Ricerca
SHOPS = {
    "Tannico": "https://www.tannico.it/catalogsearch/result/?q=",
    "Bernabei": "https://www.bernabei.it/catalogsearch/result/?q=",
    "Vino.com": "https://www.vino.com/search?q=",
    "Callmewine": "https://www.callmewine.com/catalogsearch/result/?q="
}

# --- CARICAMENTO DATI ---
uploaded_file = st.file_uploader("Carica Excel (legge tutte le schede)", type=['xlsx'])
manual_wine = st.text_input("Inserimento rapido singola etichetta")

vini = []

# Funzione per leggere TUTTI i fogli dell'Excel
if uploaded_file:
    fogli = pd.read_excel(uploaded_file, sheet_name=None)
    for nome_foglio, df in fogli.items():
        if not df.empty:
            # Prende i dati dalla prima colonna di ogni foglio
            vini.extend(df.iloc[:, 0].dropna().astype(str).tolist())

if manual_wine:
    vini.append(manual_wine)

# --- GENERAZIONE INTERFACCIA ---
if vini:
    vini = list(dict.fromkeys(vini)) # Rimuove i duplicati
    st.success(f"✅ Trovate {len(vini)} etichette totali da tutte le schede del file.")
    
    st.info("Clicca sui pulsanti per aprire la ricerca. Il tuo browser caricherà i risultati reali senza blocchi.")

    for v in vini:
        # Crea una riga espandibile per ogni vino
        with st.expander(f"🛒 Confronta prezzi per: {v}", expanded=True):
            cols = st.columns(len(SHOPS))
            for i, (name, base_url) in enumerate(SHOPS.items()):
                # Crea il link di ricerca sicuro
                link = f"{base_url}{urllib.parse.quote(v.strip())}"
                # Bottone cliccabile che apre una nuova scheda
                cols[i].link_button(f"Cerca su {name}", link, use_container_width=True)

else:
    st.write("Inizia caricando un file Excel o inserendo un vino manualmente.")
