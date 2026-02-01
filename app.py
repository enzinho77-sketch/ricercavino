import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="VinoFinder Fast", layout="wide")

st.title("🍷 VinoFinder Fast - No Blocks")
st.markdown("I siti bloccano i software? Risolviamo aprendo le ricerche direttamente nel tuo browser.")

SHOPS = {
    "Tannico": "https://www.tannico.it/catalogsearch/result/?q=",
    "Bernabei": "https://www.bernabei.it/catalogsearch/result/?q=",
    "Vino.com": "https://www.vino.com/search?q=",
    "Callmewine": "https://www.callmewine.com/catalogsearch/result/?q="
}

uploaded_file = st.file_uploader("Carica Excel (tutte le schede)", type=['xlsx'])
manual_wine = st.text_input("Inserimento rapido")

vini = []
if uploaded_file:
    fogli = pd.read_excel(uploaded_file, sheet_name=None)
    for f in fogli.values():
        vini.extend(f.iloc[:, 0].dropna().astype(str).tolist())
if manual_wine:
    vini.append(manual_wine)

if vini:
    vini = list(dict.fromkeys(vini))
    st.success(f"Trovate {len(vini)} etichette. Clicca sui link per aprire la ricerca reale.")
    
    for v in vini:
        with st.expander(f"🛒 Controlla prezzi per: {v}", expanded=True):
            cols = st.columns(len(SHOPS))
            for i, (name, base_url) in enumerate(SHOPS.items()):
                link = f"{base_url}{urllib.parse.quote(v)}"
                cols[i].markdown(f"[Vai su **{name}**]({link})")

st.info("Consiglio: Usa il tasto destro del mouse e clicca 'Apri in una nuova scheda' sui nomi dei siti per confrontarli velocemente.")
