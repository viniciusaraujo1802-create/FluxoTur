import streamlit as st
import random

st.set_page_config(page_title="FLUXOTUR", layout="wide")

# --- CSS COM A SUA IMAGEM ---
def set_style():
    # URL direta da imagem que você forneceu
    bg_url = "https://i.ibb.co/nq73snyt/download.jpg"
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Fundo branco semitransparente para garantir leitura */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
    }}
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

set_style()

# --- BASE DE DADOS FIXA (Sem randomização errada) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": "Esporte",
    "Aguaray Eco": "Natureza",
    "Amanhecer nas Cataratas": "Natureza",
    "AquaFoz": "Cultura",
    "Aquamania": "Lazer",
    "Bike Poço Preto": "Esporte",
    "Blue Park": "Lazer",
    "Cataratas del Iguazú – Argentina": "Natureza",
    "Cataratas do Iguaçu – Brasil": "Natureza",
    "Céu das Cataratas": "Experiência",
    "Circuito São João": "Cultura",
    "Dreams Park Show": "Lazer",
    "Falls Bike Tour": "Esporte",
    "Fly Foz – Paraquedismo": "Esporte",
    "Helisul Experience": "Experiência",
    "Iguassu By Bike": "Esporte",
    "Iguassu River Tour": "Natureza",
    "Iguassu Secret Falls": "Natureza",
    "Iguazu Wellness": "Experiência",
    "Itaipu Especial": "Cultura",
    "Itaipu Iluminada": "Cultura",
    "Itaipu Panorâmica": "Cultura",
    "Itaipu Refúgio Biológico": "Natureza",
    "Kattamaram": "Lazer",
    "Macuco Safari": "Esporte",
    "Marco das Três Fronteiras": "Cultura",
    "Mesquita Omar Ibn Al-Khattab": "Cultura",
    "Parque das Aves": "Natureza",
    "Pôr do Sol nas Cataratas": "Natureza",
    "Templo Budista Chen Tien": "Cultura",
    "Turismo Itaipu": "Cultura",
    "Wonder Park Foz": "Lazer",
    "Yup Star – Roda Gigante": "Lazer"
}

# --- LÓGICA DE BUSCA PRECISA ---
def filtrar_atrativos(termo):
    termo = termo.capitalize()
    # Mapeamento para garantir que "Igreja" ou outros sinônimos caiam na categoria certa
    mapeamento = {"Igreja": "Cultura", "Templo": "Cultura", "Mesquita": "Cultura"}
    categoria_busca = mapeamento.get(termo, termo)
    
    return {n: c for n, c in atrativos_db.items() if categoria_busca.lower() == c.lower()}

# --- INTERFACE ---
st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico")
st.markdown("**Categorias:** *Natureza, Esporte, Cultura, Lazer, Experiência*")

pesquisa = st.text_input("💬 O que você deseja fazer hoje?")

if pesquisa:
    resultado = filtrar_atrativos(pesquisa)
    if not resultado:
        st.warning("Não encontrei atrativos para esse termo. Tente uma das categorias acima.")
    else:
        st.success(f"Encontrei {len(resultado)} opções para '{pesquisa}':")
        if st.button("🚀 Gerar Rota Otimizada"):
            for nome, cat in resultado.items():
                st.markdown(f"### {nome}")
                st.write(f"**Categoria:** {cat}")
                st.markdown("---")
