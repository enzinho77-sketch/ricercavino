import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="VinoFinder 2.0", layout="wide")

st.title("🍷 Ricerca Vino 2.0 (Modalità Infallibile)")
st.markdown("Questa versione usa la potenza di Google per trovare i vini direttamente dentro gli e-commerce scelti, superando ogni blocco.")

# Configurazione Siti
shops = {
    "Tannico": "tannico.it",
    "Bernabei": "bernabei.it",
    "Vino.com": "vino.com",
    "Callmewine": "callmewine.com"
}

# Funzione per creare il link di ricerca tramite Google
def crea_google_link(site, vino):
    query = f"site:{site} {vino}"
    query_encoded = urllib.parse.quote(query)
    return f"https://www.google.com/search?q={query_encoded}"

# --- INTERFACCIA ---
col1, col2 = st.columns(2)
with col1:
    manual_wine = st.text_input("Inserisci etichetta (es: Sassicaia 2018)")
with col2:
    uploaded_file = st.file_uploader("Carica Excel", type=['xlsx', 'csv'])

vini = []
if manual_wine: vini.append(manual_wine)
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    vini.extend(df.iloc[:, 0].dropna().tolist())

if vini:
    st.divider()
    cols = st.columns(len(shops))
    
    for idx, (shop_name, domain) in enumerate(shops.items()):
        with cols[idx]:
            st.subheader(shop_name)
            for v in vini:
                link = crea_google_link(domain, v)
                st.markdown(f"🔍 **[{v}]({link})**")
            st.divider()
