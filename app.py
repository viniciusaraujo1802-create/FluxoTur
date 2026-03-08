import streamlit as st
import random

# Configuração da página (deve ser o primeiro comando do Streamlit)
st.set_page_config(page_title="FLUXOTUR", layout="wide")

# --- CSS PARA O FUNDO E CONTRASTE ---
# Usando a URL direta da imagem para garantir que ela carregue na nuvem
def set_style():
    bg_url = "https://files.fm/thumb_show.php?i=2k4txcan9j" # Link direto da sua imagem
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Fundo branco semitransparente para garantir que o texto apareça */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
    }}
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

set_style()

# --- INTERFACE ---
st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico – Foz do Iguaçu")

# Exibindo as categorias de forma clara
st.markdown("**Categorias disponíveis:** *Natureza, Esporte, Cultura, Lazer, Experiência*")

pesquisa = st.text_input("💬 O que você deseja fazer hoje?")

if st.button("🚀 Gerar Rota Otimizada"):
    # Sua lógica de processamento continua aqui
    st.write("Processando sua rota...")
