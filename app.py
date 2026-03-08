import streamlit as st
import random
import base64

# Configuração da página
st.set_page_config(page_title="FLUXOTUR", layout="wide")

# --- FUNÇÃO DE ESTILO (Fundo Cataratas) ---
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp {{ background-color: rgba(255, 255, 255, 0.7); }}
        div[data-testid="stExpander"] {{ background-color: rgba(255, 255, 255, 0.95); }}
        h1, h2, h3, p, label {{ color: #000000 !important; font-weight: bold; }}
        </style>
        """
        st.markdown(style, unsafe_html=True)
    except:
        st.warning("Certifique-se que o arquivo 'foz.jpg' está na mesma pasta do código.")

set_background("foz.jpg")

# --- BASE DE DADOS (33 Atrativos) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": "Esporte, kart indoor, profissional.",
    "Aguaray Eco": "Natureza, trilha, cachoeiras.",
    "Amanhecer nas Cataratas": "Natureza, experiência, exclusivo, sol.",
    "AquaFoz": "Cultura, aquário, espécies.",
    "Aquamania": "Lazer, parque aquático, toboáguas.",
    "Bike Poço Preto": "Esporte, cicloturismo, natureza.",
    "Blue Park": "Lazer, parque aquático, termal.",
    "Cataratas del Iguazú – Argentina": "Natureza, turismo, Argentina.",
    "Cataratas do Iguaçu – Brasil": "Natureza, turismo, principal.",
    "Céu das Cataratas": "Experiência, aéreo, exclusivo.",
    "Circuito São João": "Cultura, passeio, regional.",
    "Dreams Park Show": "Lazer, museu, cera, atrações.",
    "Falls Bike Tour": "Esporte, bicicleta, guiado.",
    "Fly Foz – Paraquedismo": "Esporte, adrenalina, paraquedismo.",
    "Helisul Experience": "Experiência, helicóptero, Cataratas.",
    "Iguassu By Bike": "Esporte, cicloturismo, urbano.",
    "Iguassu River Tour": "Natureza, barco, Rio Iguaçu.",
    "Iguassu Secret Falls": "Natureza, expedição, cachoeiras.",
    "Iguazu Wellness": "Experiência, yoga, bem-estar.",
    "Itaipu Especial": "Cultura, técnico, usina.",
    "Itaipu Iluminada": "Cultura, show, luzes.",
    "Itaipu Panorâmica": "Cultura, visita, usina.",
    "Itaipu Refúgio Biológico": "Natureza, conservação, ambiental.",
    "Kattamaram": "Lazer, barco, Lago de Itaipu.",
    "Macuco Safari": "Esporte, adrenalina, barco.",
    "Marco das Três Fronteiras": "Cultura, encontro, três países.",
    "Mesquita Omar Ibn Al-Khattab": "Cultura, arquitetura, religiosa.",
    "Parque das Aves": "Natureza, conservação, aves.",
    "Pôr do Sol nas Cataratas": "Natureza, experiência, pôr do sol.",
    "Templo Budista Chen Tien": "Cultura, templo, budismo.",
    "Turismo Itaipu": "Cultura, oficial, visita.",
    "Wonder Park Foz": "Lazer, interativo, complexo.",
    "Yup Star – Roda Gigante": "Lazer, roda gigante, vista."
}

# --- FUNÇÕES ---
def extrair_categoria(frase):
    frase = frase.lower()
    if any(x in frase for x in ["natureza", "trilha", "cachoeira", "eco", "parque", "selva", "árvore", "verde", "rio", "água", "refúgio", "biológico", "animal", "aves", "ao ar livre"]): return "Natureza"
    if any(x in frase for x in ["esporte", "kart", "bike", "bicicleta", "cicloturismo", "paraquedismo", "adrenalina", "salto", "radical", "ativo", "exercício", "pedalar"]): return "Esporte"
    if any(x in frase for x in ["cultura", "igreja", "templo", "mesquita", "história", "histórico", "técnico", "usina", "museu", "arquitetura", "religioso", "tradição", "cidade"]): return "Cultura"
    if any(x in frase for x in ["lazer", "diversão", "parque aquático", "família", "criança", "passeio", "termal", "roda gigante", "show", "barco", "cruzeiro"]): return "Lazer"
    if any(x in frase for x in ["experiência", "yoga", "wellness", "relaxar", "exclusivo", "pôr do sol", "nascer do sol", "bem-estar", "helicóptero", "vista", "panorâmica"]): return "Experiência"
    return "Geral"

# --- INTERFACE ---
st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico – Foz do Iguaçu")
st.markdown("**Categorias:** *Natureza, Esporte, Cultura, Lazer, Experiência*")

pesquisa = st.text_input("💬 O que você deseja fazer hoje?")

if pesquisa:
    cat = extrair_categoria(pesquisa)
    st.write(f"🔍 Exibindo: **{cat}**")
    lista_exibir = {n: d for n, d in atrativos_db.items() if cat.lower() in d.lower() or cat == "Geral"}
else:
    lista_exibir = atrativos_db

if st.button("🚀 Gerar Rota Otimizada"):
    for nome, desc in lista_exibir.items():
        with st.expander(f"{nome}"):
            st.write(f"**Descrição:** {desc}")
            if "Kartódromo" in nome:
                st.image("https://files.fm/thumb_show.php?i=ctv2gsd6ga", caption="Adrena Kart Foz")
