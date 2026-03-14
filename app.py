import streamlit as st
import random
import pandas as pd

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS CORRIGIDO ---
def injetar_vlibras():
    vlibras_html = """
    <div vw class="enabled">
        <div vw-access-button class="active"></div>
        <div vw-plugin-wrapper>
            <div class="vw-plugin-top-wrapper"></div>
        </div>
    </div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>
        new window.VLibras.Widget('https://vlibras.gov.br/app');
    </script>
    <style>
        [vw] {
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            z-index: 999999 !important;
        }
    </style>
    """
    st.markdown(vlibras_html, unsafe_allow_html=True)

injetar_vlibras()

def gerar_link_mapas(nome):
    return f"https://www.google.com/maps/search/?api=1&query={nome.replace(' ', '+')}+Foz+do+Iguacu"

# --- CSS ---
st.markdown("""
<style>
.stApp { background-image: url("https://i.ibb.co/nq73snyt/download.jpg"); background-size: cover; background-attachment: fixed; }
.block-container { background-color: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; }
h1, h2, h3, p, label { color: #000000 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS COMPLETA (33 ATRATIVOS) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "dica": "Sinta a adrenalina na pista."},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "dica": "Trilhas e cachoeiras revigorantes."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Uma visão exclusiva do despertar das águas."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "lat": -25.616, "lon": -54.481, "dica": "Mergulhe na biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "lat": -25.538, "lon": -54.542, "dica": "Diversão aquática para toda a família."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "lat": -25.695, "lon": -54.436, "dica": "Explore a floresta sobre duas rodas."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "dica": "Relaxe nas águas termais com ondas."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "lat": -25.684, "lon": -54.444, "dica": "A imponência das quedas pelo lado hermano."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "A vista clássica da Garganta do Diabo."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "lat": -25.695, "lon": -54.436, "dica": "Uma experiência gastronômica nas alturas."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "lat": -25.510, "lon": -54.500, "dica": "Conheça as raízes da comunidade local."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "lat": -25.565, "lon": -54.502, "dica": "Um mundo de magia e museus temáticos."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "lat": -25.695, "lon": -54.436, "dica": "Pedale próximo às grandes quedas."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "lat": -25.534, "lon": -54.545, "dica": "Salte e veja tudo do céu."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "lat": -25.692, "lon": -54.438, "dica": "Voo panorâmico inesquecível."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "lat": -25.550, "lon": -54.580, "dica": "Passeios guiados de bicicleta."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "lat": -25.690, "lon": -54.435, "dica": "Navegue pelas águas do rio Iguaçu."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "lat": -25.550, "lon": -54.550, "dica": "Descubra cachoeiras escondidas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "lat": -25.560, "lon": -54.520, "dica": "Relaxe e renove suas energias."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "dica": "A visita técnica mais completa da usina."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Veja a usina brilhar à noite."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "lat": -25.405, "lon": -54.588, "dica": "A vista clássica da gigante Itaipu."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "lat": -25.410, "lon": -54.550, "dica": "Preservação da fauna e flora regional."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "lat": -25.405, "lon": -54.588, "dica": "Passeio de barco relaxante."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Banho de cachoeira radical."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "dica": "O ponto onde os países se encontram."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "lat": -25.535, "lon": -54.575, "dica": "Arquitetura e cultura islâmica."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "dica": "Imersão no mundo das aves tropicais."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "O espetáculo final do dia."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "lat": -25.534, "lon": -54.550, "dica": "Paz e reflexão em um lugar único."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Explore todas as faces da usina."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "lat": -25.550, "lon": -54.540, "dica": "Cinema e shows temáticos."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "dica": "Vista panorâmica da cidade."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    st.markdown("Olá! Sou o X.Tur, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/).")
    
    st.markdown("💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
    
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    btn_clicado = st.button("🚀 Gerar roteiro inteligente")
    
    if btn_clicado or pesquisa:
        with st.spinner("Analis
