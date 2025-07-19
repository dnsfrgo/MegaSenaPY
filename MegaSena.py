# mega_sena_app.py
import streamlit as st
import kagglehub
import pandas as pd
import os
from collections import Counter

# --- App Title and Header ---
st.set_page_config(page_title="🔮 Mega-Sena Predictions", page_icon="🇧🇷")
st.title("🤑 Brazil - Mega-Sena Predictor [Para Gui]")
st.write("Este aplicativo analisa a frequência histórica dos resultados da Mega-Sena para gerar 3 linhas de jogo.\n\n\n"
        "Como a análise é baseada em dados, os números gerados não são aleatórios e serão sempre os mesmos.\n\n"
         "**Linha 1 (Mais Frequentes):** Os 6 números mais sorteados na história.\n\n"
        "**Linha 2 (Nível 2):** Os próximos 6 números da lista de mais sorteados (do 7º ao 12º).\n\n"
        "**Linha 3 (Nível 3):** O terceiro conjunto de 6 números mais sorteados (do 13º ao 18º).\n\n")

# --- Data Loading Function ---
@st.cache_data(ttl="1d")
def load_data():
    """Loads the Brazil Mega-Sena dataset from Kaggle."""
    dataset_path = "danttis/brazil-lottery-mega-sena"
    try:
        path = kagglehub.dataset_download(dataset_path)
        csv_path = next((os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")), None)
        return pd.read_csv(csv_path) if csv_path else None
    except Exception as e:
        st.error(f"Failed to download data from Kaggle. Error: {e}")
        return None


# --- Function to Display Results (simplified for no bonus ball) ---
def display_results(df, main_cols):
    """Processes and displays the top 3 tiered lines."""
    try:
        all_main_numbers = df[main_cols].values.flatten()
        main_freq = Counter(all_main_numbers)
        top_18_main_numbers = [item[0] for item in main_freq.most_common(18)]

        st.header("Linhas Previstas (Com Base na Frequência Histórica)")

        # Tier 1
        line1_main = sorted(top_18_main_numbers[0:6])
        st.subheader("Linha 1 (Mais Frequentes):")
        st.markdown(f"**{', '.join(str(int(x)) for x in line1_main)}**")

        # Tier 2
        line2_main = sorted(top_18_main_numbers[6:12])
        st.subheader("Linha 2 (Nível 2):")
        st.markdown(f"**{', '.join(str(int(x)) for x in line2_main)}**")

        # Tier 3
        line3_main = sorted(top_18_main_numbers[12:18])
        st.subheader("Linha 3 (Nível 3):")
        st.markdown(f"**{', '.join(str(int(x)) for x in line3_main)}**")

    except Exception as e:
        st.error(f"Could not process the data. Please check the column names. Error: {e}")


# --- Main App Logic ---
# Set credentials from Streamlit Secrets
try:
    os.environ['KAGGLE_USERNAME'] = st.secrets["KAGGLE_USERNAME"]
    os.environ['KAGGLE_KEY'] = st.secrets["KAGGLE_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Kaggle credentials not found in Streamlit Secrets. Please add them to your app's settings.")
    st.stop()

# Load the data and display the results
df = load_data()
if df is not None:
    # Column names based on your screenshot for Mega-Sena
    main_cols = ['Ball1', 'Ball2', 'Ball3', 'Ball4', 'Ball5', 'Ball6']
    display_results(df, main_cols)
else:
    st.warning("Could not load data to display results.")