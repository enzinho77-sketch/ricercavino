import streamlit as st
import pandas as pd
import urllib.parse

# Configurazione Pagina
st.set_page_config(page_title="Ricerca Vino 2.0", layout="wide")

st.title("🍷 Ricerca Vino 2.0")
st.markdown("Genera istantaneamente link di ricerca per i migliori e-commerce.")

# Configurazione URL di ricerca per i 4 siti
shops = {
    "Tannico": "https://www.tannico.it/catalogsearch/result/?q=",
    "Bernabei": "https://www.bernabei.it/catalogsearch/result/?q=",
    "Vino.com": "https://www.vino.com/search?q=",
    "Callmewine": "https://www.callmewine.com/catalogsearch/result/?q="
}

# Interfaccia di Input
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Ricerca Singola")
    manual_wine = st.text_input("Inserisci etichetta (es: Sassicaia 2018)")

with col2:
    st.subheader("📂 Carica Lista")
    uploaded_file = st.file_uploader("Carica Excel o CSV", type=['xlsx', 'csv'])

# Preparazione lista vini
vini_da_cercare = []
if manual_wine:
    vini_da_cercare.append(manual_wine)

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        vini_da_cercare.extend(df.iloc[:, 0].dropna().tolist())
    except Exception as e:
        st.error("Errore nel caricamento del file. Controlla il formato.")

# Visualizzazione Risultati
if vini_da_cercare:
    st.divider()
    st.info(f"Clicca sui nomi per aprire la ricerca su ogni sito. (Trovati {len(vini_da_cercare)} vini)")
    
    # Creiamo una colonna per ogni negozio
    cols = st.columns(len(shops))
    
    for idx, (shop_name, base_url) in enumerate(shops.items()):
        with cols[idx]:
            st.header(shop_name)
            for vino in vini_da_cercare:
                # Pulizia e creazione link
                query = urllib.parse.quote(str(vino).strip())
                link_finale = base_url + query
                
                # Bottone/Link elegante
                st.markdown(f"👉 **[{vino}]({link_finale})**")
                st.divider()

else:
    st.write("Inizia inserendo un vino o caricando un file.")
