import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="VinoFinder Fast", layout="wide")

st.title("🍷 VinoFinder Fast - No Blocks")
st.markdown("I siti bloccano i robot? Risolviamo aprendo le ricerche direttamente nel tuo browser.")

SHOPS = {
    "Tannico": "https://www.tannico.it/catalogsearch/result/?q=",
    "Bernabei": "https://www.bernabei.it/catalogsearch/result/?q=",
    "Vino.com": "https://www.vino.com/search?q=",
    "Callmewine": "https://www.callmewine.com/catalogsearch/result/?q="
}

# Funzione per pulire il nome del vino
def pulisci_nome(nome):
    return str(nome).strip()

uploaded_file = st.file_uploader("Carica Excel (legge tutte le schede)", type=['xlsx'])
manual_wine = st.text_input("Inserimento rapido singola etichetta")

vini = []
if uploaded_file:
    fogli = pd.read_excel(uploaded_file, sheet_name=None)
    for nome_foglio, df in fogli.items():
        if not df.empty:
            # Prende la prima colonna di ogni foglio
            vini.extend(df.iloc[:, 0].dropna().tolist())

if manual_wine:
    vini.append(manual_wine)

if vini:
    vini = list(dict.fromkeys(vini)) # Rimuove duplicati
    st.success(f"✅ Trovate {len(vini)} etichette totali da tutte le schede.")
    
    # Creazione della tabella di controllo
    for v in vini:
        nome_v = pulisci_nome(v)
        with st.expander(f"🛒 Confronta: {nome_v}", expanded=True):
            cols = st.columns(len(SHOPS))
            for i, (name, base_url) in enumerate(SHOPS.items()):
                link = f"{base_url}{urllib.parse.quote(nome_v)}"
                cols[i].markdown(f"**{name}**")
                cols[i].link_button(f"Cerca su {name}", link)

st.divider()
st.info("💡 **Consiglio Pro:** Carica l'Excel e clicca sui pulsanti per aprire le schede. Il tuo browser non verrà mai bloccato perché la ricerca parte dal tuo indirizzo IP reale.")
