import streamlit as st
import pd as pd
import urllib.parse
import re

st.set_page_config(page_title="VinoFinder 3.0", layout="wide", page_icon="🍷")

# --- LOGICA DI PULIZIA SMART ---
def normalizza_nome_vino(nome):
    """Pulisce il nome per massimizzare i risultati sui siti italiani."""
    if not isinstance(nome, str): return str(nome)
    
    # Trasforma in maiuscolo per uniformità
    n = nome.upper()
    
    # Rimuove termini tecnici che bloccano i motori di ricerca interni
    scarti = [
        r'\bDOCG\b', r'\bDOC\b', r'\bIGT\b', r'\bVDP\b', 
        r'\bCL\.?75\b', r'\b75\s?CL\b', r'\b0\.75\b', r'\bLT\b',
        r'\bASTUCCIATO\b', r'\bCASSA\b', r'\bLEGNO\b', r'\bOWC\b'
    ]
    for pattern in scarti:
        n = re.sub(pattern, '', n)
    
    # Pulizia finale spazi e punteggiatura
    n = re.sub(r'[^\w\s]', ' ', n)
    return " ".join(n.split()).title()

# --- CONFIGURAZIONE ---
SHOPS = {
    "Tannico": "https://www.tannico.it/catalogsearch/result/?q=",
    "Bernabei": "https://www.bernabei.it/catalogsearch/result/?q=",
    "Vino.com": "https://www.vino.com/search?q=",
    "Callmewine": "https://www.callmewine.com/catalogsearch/result/?q="
}

st.title("🍷 VinoFinder 3.0 - Smart Assistant")
st.markdown("Analisi dei dati ispirata ai sistemi di normalizzazione di **Wine-Searcher**.")

# --- STEP 1: CARICAMENTO ---
uploaded_file = st.file_uploader("Carica il tuo Excel (legge tutti i fogli)", type=['xlsx'])

if uploaded_file:
    # Lettura completa
    dict_fogli = pd.read_excel(uploaded_file, sheet_name=None)
    grezzi = []
    for df in dict_fogli.values():
        if not df.empty:
            grezzi.extend(df.iloc[:, 0].dropna().tolist())
    
    vini_unici = sorted(list(set(grezzi)))
    
    # --- STEP 2: ANTEPRIMA PULIZIA ---
    st.header("⚙️ Anteprima Pulizia Nomi")
    st.info("Abbiamo rimosso termini come 'DOCG', '75cl' e 'Cassa Legno' per facilitare i motori di ricerca dei siti.")
    
    # Creazione tabella comparativa
    data_preview = []
    for v in vini_unici:
        data_preview.append({"Nome Originale": v, "Nome Pulito (Ricerca)": normalizza_nome_vino(v)})
    
    df_preview = pd.DataFrame(data_preview)
    st.table(df_preview.head(10)) # Mostra i primi 10 per controllo
    
    if len(df_preview) > 10:
        st.write(f"...e altri {len(df_preview)-10} vini.")

    # --- STEP 3: GENERAZIONE DASHBOARD ---
    st.divider()
    st.header("🚀 Centrale Operativa")
    
    for _, row in df_preview.iterrows():
        originale = row["Nome Originale"]
        pulito = row["Nome Pulito (Ricerca)"]
        
        with st.expander(f"🛒 {pulito} (Originale: {originale})"):
            cols = st.columns(4)
            for i, (nome_shop, base_url) in enumerate(SHOPS.items()):
                url_finale = f"{base_url}{urllib.parse.quote(pulito)}"
                cols[i].link_button(f"Cerca su {nome_shop}", url_finale, use_container_width=True)

else:
    st.info("Trascina un file Excel per iniziare l'analisi.")

