import streamlit as st
import pandas as pd
import urllib.parse
import re

st.set_page_config(page_title="VinoFinder - Raggruppamento Acquisti", layout="wide")

st.title("🍷 Raggruppamento per E-commerce")
st.markdown("Scegli un negozio e clicca sui nomi. Se vedi 'Nessun risultato', passa subito al successivo.")

def pulisci_nome_vino(nome):
    if not isinstance(nome, str): return ""
    n = nome.upper()
    n = re.sub(r'\b(DOCG|DOC|IGT|CL75|75CL|0\.75|LT|ASTUCCIATO|CASSA|LEGNO|MAGNUM)\b', '', n)
    n = re.sub(r'[^A-Z0-9\s]', ' ', n)
    return " ".join(n.split()).title()

# --- CARICAMENTO ---
uploaded_file = st.sidebar.file_uploader("Carica Excel", type=['xlsx'])
vini_totali = []

if uploaded_file:
    dict_fogli = pd.read_excel(uploaded_file, sheet_name=None)
    for df in dict_fogli.values():
        if not df.empty:
            vini_totali.extend(df.iloc[:, 0].dropna().astype(str).tolist())
    vini_totali = sorted(list(set(vini_totali)))

# --- INTERFACCIA A TAB (RAGGRUPPATA) ---
if vini_totali:
    # Selettore negozio per non avere mille tasti sparsi
    negozio = st.selectbox("Seleziona l'e-commerce su cui vuoi acquistare ora:", 
                           ["tannico.it", "bernabei.it", "vino.com", "callmewine.com"])
    
    st.write(f"### Lista vini da cercare su {negozio}")
    
    # Griglia compatta per scansione rapida
    cols = st.columns(4)
    for i, v in enumerate(vini_totali):
        v_p = pulisci_nome_vino(v)
        query = f'site:{negozio} "{v_p}"'
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query) + "&tbs=li:1"
        
        # Il tasto apre la ricerca Sniper
        cols[i % 4].link_button(v_p, url, use_container_width=True)
else:
    st.info("Carica l'Excel per iniziare.")
