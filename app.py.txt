import streamlit as st
import pandas as pd
import requests
import random
import time
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# -----------------------
# Config
# -----------------------
st.set_page_config(
    page_title="VinoFinder Pro",
    layout="wide"
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

HEADERS = lambda: {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "it-IT,it;q=0.9"
}

SITES = {
    "Tannico": {
        "url": "https://www.tannico.it/catalogsearch/result/?q={query}",
        "no_result_keywords": ["Nessun prodotto", "non ha prodotto risultati"]
    },
    "Bernabei": {
        "url": "https://www.bernabei.it/search?controller=search&s={query}",
        "no_result_keywords": ["0 risultati", "Nessun risultato"]
    },
    "Vino.com": {
        "url": "https://www.vino.com/ricerca?search={query}",
        "no_result_keywords": ["Nessun prodotto", "0 prodotti"]
    },
    "Callmewine": {
        "url": "https://www.callmewine.com/search?q={query}",
        "no_result_keywords": ["Nessun prodotto", "non ha prodotto risultati"]
    },
}

TIMEOUT = 10

# -----------------------
# Funzioni
# -----------------------
def check_wine(site_name, site_data, wine_name):
    query = quote_plus(wine_name)
    url = site_data["url"].format(query=query)

    try:
        r = requests.get(url, headers=HEADERS(), timeout=TIMEOUT)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        for kw in site_data["no_result_keywords"]:
            if kw.lower() in text:
                return None

        return url

    except Exception:
        return None


def load_wines_from_file(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    if len(df.columns) == 1:
        return df.iloc[:, 0].dropna().astype(str).tolist()

    col = st.selectbox("Seleziona la colonna con i nomi dei vini", df.columns)
    return df[col].dropna().astype(str).tolist()


# -----------------------
# UI
# -----------------------
st.title("🍷 VinoFinder Pro")
st.write("Ricerca rapida disponibilità vini su e-commerce italiani.")

manual_wine = st.text_input("Inserisci un vino manualmente")

uploaded_file = st.file_uploader(
    "Oppure carica un file CSV o Excel",
    type=["csv", "xlsx"]
)

wine_list = []

if manual_wine:
    wine_list.append(manual_wine.strip())

if uploaded_file:
    wine_list.extend(load_wines_from_file(uploaded_file))

wine_list = list(dict.fromkeys(wine_list))  # rimuove duplicati

if st.button("Avvia ricerca") and wine_list:
    progress = st.progress(0)
    total = len(wine_list) * len(SITES)
    step = 0

    results = {site: [] for site in SITES}

    for wine in wine_list:
        for site, data in SITES.items():
            link = check_wine(site, data, wine)
            step += 1
            progress.progress(step / total)

            if link:
                results[site].append((wine, link))

            time.sleep(0.3)  # educato, non fare il barbaro

    st.success("Ricerca completata")

    cols = st.columns(len(SITES))

    for col, (site, items) in zip(cols, results.items()):
        with col:
            st.subheader(site)
            if not items:
                st.caption("Nessun risultato")
            for wine, link in items:
                st.markdown(f"- [{wine}]({link})", unsafe_allow_html=True)

else:
    st.info("Inserisci almeno un vino o carica un file.")
