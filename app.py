import streamlit as st
import random

st.set_page_config(page_title="FLUXOTUR", layout="wide")

# --- FUNÇÃO DE ESTILO COM URL DIRETA ---
def set_style():
    # COLE O LINK DIRETO DA IMAGEM AQUI (deve terminar em .jpg)
    bg_url = "LINK_DIRETO_DA_IMAGEM_AQUI" 
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
    }}
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

set_style()

# --- (O RESTANTE DO SEU CÓDIGO PERMANECE O MESMO) ---
# ... insira a base de dados e a interface abaixo ...
