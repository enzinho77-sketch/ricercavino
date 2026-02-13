import streamlit as st
import pandas as pd
import urllib.parse
import re

st.set_page_config(page_title="VinoFinder - Power Shopper", layout="wide")

st.title("🚀 Power Shopper: Raggruppamento E-Commerce")
st.markdown("""
1. Seleziona il negozio. 
2. Clicca sui vini: si apriranno in nuove schede.
3. Se vedi la pagina di errore di Google, chiudi la scheda (CTRL+W) e passa al prossimo.
""")

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

# --- INTERFACCIA DI ACQUISTO ---
if vini_totali:
    # SELETTORE NEGOZIO
    shop = st.radio("Scegli dove vuoi acquistare ora:", 
                    ["tannico.it", "bernabei.it", "vino.com", "callmewine.com"], 
                    horizontal=True)
    
    filtro = st.text_input("Filtra lista (es: Abruzzo, 2023...)")
    vini_filtrati = [v for v in vini_totali if filtro.lower() in v.lower()] if filtro else vini_totali

    st.write(f"### {len(vini_filtrati)} vini pronti per {shop}")
    
    # Visualizzazione compatta a tabelle per raggruppare l'acquisto
    # Usiamo dei checkbox per segnare quelli che hai già verificato/comprato
    for i in range(0, len(vini_filtrati), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(vini_filtrati):
                v_orig = vini_filtrati[i+j]
                v_p = pulisci_nome_vino(v_orig)
                query = f'site:{shop} "{v_p}"'
                url = "https://www.google.com/search?q=" + urllib.parse.quote(query) + "&tbs=li:1"
                
                with cols[j]:
                    st.link_button(f"🔍 {v_p}", url, use_container_width=True)
                    st.checkbox("Preso", key=f"{shop}_{v_orig}") # Ti aiuta a non perdere il segno
else:
    st.info("Carica l'Excel per iniziare.")
