# mega_sena_app.py
import streamlit as st
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


# --- Botão de atualização em Português ---
if st.button("Verificar Atualizações e Atualizar Dados 🔄 "):
    # Limpa todas as funções em cache
    st.cache_data.clear()
    # Mensagem de sucesso em Português
    st.success("Cache de dados limpo! Atualizando os números...")
    # Roda o app desde o início
    st.rerun()

# --- Data Loading Function ---
@st.cache_data(ttl="1d")
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR61gQrKotrJhGDVRCafMj0K15Pvv7TLaayeTIuQan7YE2EAFPBMlUk9zZdR444IUqNUhXRh46hlNVb/pub?gid=1514261907&single=true&output=csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load Google Sheet. Error: {e}")
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


# Load the data and display the results
df = load_data()
if df is not None:
    # Clean column names just in case
    df.columns = df.columns.str.strip()

    main_cols = ['Ball1', 'Ball2', 'Ball3', 'Ball4', 'Ball5', 'Ball6']

    # Convert Date column to datetime using the right dayfirst format
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    most_recent_date = df['Date'].max()

    if pd.isna(most_recent_date):
        st.warning("Não foi possível identificar a data mais recente.")
    else:
        formatted_date = most_recent_date.strftime("%d/%m/%Y")
        st.info(f"📅 Data do jogo mais recente: **{formatted_date}**")

    # Display it in the app with a Portuguese descriptor
    st.info(f"📅 Data do jogo mais recente: **{formatted_date}**")

    # Then show your predicted lines
    display_results(df, main_cols)
else:
    st.warning("Could not load data to display results.")
