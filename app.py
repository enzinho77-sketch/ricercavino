import streamlit as st
import pandas as pd
import urllib.parse
import re

st.set_page_config(page_title="VinoFinder Pro - Dashboard Acquisti", layout="wide")

st.title("🍷 Dashboard Acquisti Raggruppata")
st.markdown("Seleziona l'e-commerce in alto per vedere la tua lista pronta al click.")

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
    vini_totali = list(dict.fromkeys(vini_totali))
    st.sidebar.success(f"📦 {len(vini_totali)} vini caricati")

# --- DASHBOARD RAGGRUPPATA PER E-COMMERCE ---
if vini_totali:
    # Creiamo le schede per ogni negozio
    tabs = st.tabs(["🛒 Tannico", "🛒 Bernabei", "🛒 Vino.com", "🛒 Callmewine", "🛒 XtraWine"])
    
    shops_config = [
        {"name": "Tannico", "domain": "tannico.it", "tab": tabs[0]},
        {"name": "Bernabei", "domain": "bernabei.it", "tab": tabs[1]},
        {"name": "Vino.com", "domain": "vino.com", "tab": tabs[2]},
        {"name": "Callmewine", "domain": "callmewine.com", "tab": tabs[3]},
        {"name": "XtraWine", "domain": "xtrawine.com", "tab": tabs[4]},
    ]

    for shop in shops_config:
        with shop["tab"]:
            st.header(f"Lista pronta per {shop['name']}")
            st.info(f"Clicca sui nomi per verificare la disponibilità su {shop['domain']}")
            
            # Layout a griglia per acquisti rapidi
            cols = st.columns(3) 
            for i, v in enumerate(vini_totali):
                v_pulito = pulisci_nome_vino(v)
                query = f'site:{shop["domain"]} "{v_pulito}"'
                url = "https://www.google.com/search?q=" + urllib.parse.quote(query) + "&tbs=li:1"
                
                # Inseriamo i bottoni in colonna
                cols[i % 3].link_button(f"{v_pulito}", url, use_container_width=True)
else:
    st.info("Carica l'Excel per generare le liste di acquisto raggruppate.")
