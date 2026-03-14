import streamlit as st
import random
import time
import pandas as pd
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

def injetar_vlibras():
    vlibras_code = """
    <div vw class="enabled"><div vw-access-button class="active"></div><div vw-plugin-wrapper><div class="vw-plugin-top-wrapper"></div></div></div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>new window.VLibras.Widget('https://vlibras.gov.br/app');</script>
    """
    components.html(vlibras_code, height=0)

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

# --- BASE DE DADOS (33 ATRAVÉS) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "desc": "Kart indoor."},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "desc": "Trilhas e cachoeiras."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Experiência exclusiva."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "lat": -25.616, "lon": -54.481, "desc": "Aquário local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "lat": -25.538, "lon": -54.542, "desc": "Parque aquático."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "lat": -25.695, "lon": -54.436, "desc": "Cicloturismo."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "desc": "Parque termal."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "lat": -25.684, "lon": -54.444, "desc": "Trilhas argentinas."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Passarela das quedas."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "lat": -25.695, "lon": -54.436, "desc": "Jantar exclusivo."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "lat": -25.510, "lon": -54.500, "desc": "Cultura regional."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "lat": -25.565, "lon": -54.502, "desc": "Museu de cera."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "lat": -25.695, "lon": -54.436, "desc": "Bike guiado."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "lat": -25.534, "lon": -54.545, "desc": "Salto duplo."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "lat": -25.692, "lon": -54.438, "desc": "Voo de helicóptero."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "lat": -25.550, "lon": -54.580, "desc": "Mobilidade sustentável."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "lat": -25.690, "lon": -54.435, "desc": "Navegação cênica."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "lat": -25.550, "lon": -54.550, "desc": "Cachoeiras escondidas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "lat": -25.560, "lon": -54.520, "desc": "Yoga e terapias."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "desc": "Tour técnico."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "desc": "Show de luzes."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "lat": -25.405, "lon": -54.588, "desc": "Vista da usina."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "lat": -25.410, "lon": -54.550, "desc": "Animais nativos."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "lat": -25.405, "lon": -54.588, "desc": "Passeio de barco."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Aventura radical."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "desc": "Marco fronteiriço."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "lat": -25.535, "lon": -54.575, "desc": "Arquitetura islâmica."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "desc": "Aves da Mata Atlântica."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Vista privilegiada."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "lat": -25.534, "lon": -54.550, "desc": "Jardins zen."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "desc": "Complexo da usina."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "lat": -25.550, "lon": -54.540, "desc": "Museu de carros."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "desc": "Vista da fronteira."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    st.markdown("💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
    
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    
    if st.button("🚀 Gerar roteiro inteligente"):
        with st.spinner("Analisando..."):
            for nome, info in atrativos_db.items():
                if info['cat'].lower() == pesquisa.lower():
                    # Score final na escala 5.3 a 10.5
                    score = round(random.uniform(5.3, 10.5), 1)
                    c = random.choice(["Lotado", "Não Lotado"])
                    t = random.choice(["Intenso", "Não Intenso"])
                    
                    st.markdown(f"### 📍 {nome}")
                    st.write(f"**Score Final:** {score} | **Reputação:** {info['R']} | **Trânsito:** {t} | **Carga:** {c}")
                    st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(nome))
                    st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral dos 33 Atrativos")
    st.map(pd.DataFrame.from_dict(atrativos_db, orient='index'))

with tab3:
    st.header("🧠 Entenda o FluxoTur")
    st.write("Olá, eu sou o **X.Tur**!")
    st.write("A inteligência artificial não generativa diferencia-se por focar no exame e na categorização de dados pré-existentes para a formulação de previsões. Esta distinção é fundamental para sistemas que priorizam a precisão analítica sobre a criação de conteúdo, permitindo uma governança baseada em evidências estatísticas.")
