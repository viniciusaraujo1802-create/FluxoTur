import streamlit as st
import random
import pandas as pd

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS (INJEÇÃO CORRIGIDA) ---
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
        [vw] { position: fixed !important; bottom: 80px !important; right: 40px !important; z-index: 99999999 !important; }
    </style>
    """
    st.markdown(vlibras_html, unsafe_allow_html=True)

injetar_vlibras()

# --- FUNÇÕES ---
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

# --- BASE DE DADOS (33 ATRATIVOS) ---
# Renomeado 'latitude' para 'lat' e 'longitude' para 'lon' para o st.map aceitar
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "dica": "Prepare o capacete e acelere fundo!"},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "dica": "Refúgio perfeito para renovar as energias."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "O sol nascendo nas quedas."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "lat": -25.616, "lon": -54.481, "dica": "História da biodiversidade."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "lat": -25.538, "lon": -54.542, "dica": "Diversão para a família."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "lat": -25.695, "lon": -54.436, "dica": "Pedale pelo coração da floresta."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "dica": "Praia termal em Foz."},
    "Cataratas Argentina": {"cat": "Natureza", "R": 4.9, "lat": -25.684, "lon": -54.444, "dica": "O lado hermano das cataratas."},
    "Cataratas Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Garganta do Diabo."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "lat": -25.695, "lon": -54.436, "dica": "Vista espetacular."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "lat": -25.510, "lon": -54.500, "dica": "Tradições e raízes."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "lat": -25.565, "lon": -54.502, "dica": "Um mundo mágico."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "lat": -25.695, "lon": -54.436, "dica": "Vento no rosto."},
    "Fly Foz": {"cat": "Esporte", "R": 4.9, "lat": -25.534, "lon": -54.545, "dica": "Paraquedismo radical."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "lat": -25.692, "lon": -54.438, "dica": "Foto aérea única."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "lat": -25.550, "lon": -54.580, "dica": "Pontos secretos de Foz."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "lat": -25.690, "lon": -54.435, "dica": "Perspectiva do rio."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "lat": -25.550, "lon": -54.550, "dica": "Cachoeiras escondidas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "lat": -25.560, "lon": -54.520, "dica": "Bem-estar total."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "dica": "Visita técnica épica."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Show de luzes."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "lat": -25.405, "lon": -54.588, "dica": "Vista monumental."},
    "Itaipu Refúgio": {"cat": "Natureza", "R": 4.7, "lat": -25.410, "lon": -54.550, "dica": "Preservação local."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "lat": -25.405, "lon": -54.588, "dica": "Relaxe no convés."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Muita emoção!"},
    "Marco Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "dica": "Brasil, Argentina e Paraguai."},
    "Mesquita Omar": {"cat": "Cultura", "R": 4.7, "lat": -25.535, "lon": -54.575, "dica": "Arquitetura oriental."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "dica": "Aves tropicais."},
    "Pôr do Sol Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Encerramento mágico."},
    "Templo Budista": {"cat": "Cultura", "R": 4.8, "lat": -25.534, "lon": -54.550, "dica": "Paz interior."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Segredos da gigante."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "lat": -25.550, "lon": -54.540, "dica": "Tecnologia e cinema."},
    "Yup Star": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "dica": "Roda Gigante."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    if st.button("🚀 Gerar roteiro inteligente") or pesquisa:
        with st.spinner("Analisando dados..."):
            lista = [item for nome, item in atrativos_db.items() if not pesquisa or item['cat'].lower() == pesquisa.lower()]
            for item in lista:
                nome_at = [k for k, v in atrativos_db.items() if v == item][0]
                st.markdown(f"### 📍 {nome_at} ({round(random.uniform(5.3, 10.5), 1)})")
                st.info(f"💡 {item['dica']}")
                st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(nome_at))
                st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral")
    st.map(pd.DataFrame.from_dict(atrativos_db, orient='index'))

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("Sistema especialista focado em análise, triagem e recomendação de roteiros.")
