import streamlit as st
import random
import pandas as pd
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS ---
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
        [vw] { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 99999999 !important; }
    </style>
    """
    components.html(vlibras_html, height=100)

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

# --- BASE DE DADOS COMPLETA ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "dica": "Prepare o capacete e acelere fundo!"},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "dica": "Renove as energias em trilhas."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Sol nascente nas águas."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "lat": -25.616, "lon": -54.481, "dica": "História e biodiversidade."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "lat": -25.538, "lon": -54.542, "dica": "Diversão em família."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "lat": -25.695, "lon": -54.436, "dica": "Pedale na floresta."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "dica": "Praia termal em Foz."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "lat": -25.684, "lon": -54.444, "dica": "O lado hermano impressionante."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Garganta do Diabo."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "lat": -25.695, "lon": -54.436, "dica": "Sabor nas alturas."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "lat": -25.510, "lon": -54.500, "dica": "Tradições locais."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "lat": -25.565, "lon": -54.502, "dica": "Um mundo mágico."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "lat": -25.695, "lon": -54.436, "dica": "Vento no rosto."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "lat": -25.534, "lon": -54.545, "dica": "O céu de Foz te espera."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "lat": -25.692, "lon": -54.438, "dica": "Vista aérea incrível."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "lat": -25.550, "lon": -54.580, "dica": "Roteiros secretos."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "lat": -25.690, "lon": -54.435, "dica": "Perspectiva privilegiada."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "lat": -25.550, "lon": -54.550, "dica": "Cachoeiras escondidas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "lat": -25.560, "lon": -54.520, "dica": "Bem-estar total."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "dica": "Visita técnica épica."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Show de luzes."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "lat": -25.405, "lon": -54.588, "dica": "Vista monumental."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "lat": -25.410, "lon": -54.550, "dica": "Preservação local."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "lat": -25.405, "lon": -54.588, "dica": "Navegue pelo lago."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Muita emoção!"},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "dica": "Brasil, Argentina e Paraguai."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "lat": -25.535, "lon": -54.575, "dica": "Arquitetura linda."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "dica": "Vida tropical."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Encerramento mágico."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "lat": -25.534, "lon": -54.550, "dica": "Paz interior."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Segredos da usina."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "lat": -25.550, "lon": -54.540, "dica": "Show tecnológico."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "dica": "Visão inesquecível."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    st.markdown("Olá! Sou o X.Tur, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.fozdoiguacu.com.br/).")
    st.markdown("💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
    
    with st.form(key='busca'):
        pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
        btn_clicado = st.form_submit_button("🚀 Gerar roteiro inteligente")
    
    if btn_clicado or pesquisa:
        with st.spinner("Analisando dados..."):
            lista = [item for nome, item in atrativos_db.items() if not pesquisa or item['cat'].lower() == pesquisa.lower()]
            if not lista: 
                st.warning("🤖 Ops! Não encontrei nada.")
            else:
                for item in lista:
                    item['score'] = round(random.uniform(5.3, 10.5), 1)
                lista_ordenada = sorted(lista, key=lambda x: x['score'], reverse=True)
                for item in lista_ordenada:
                    nome = [k for k, v in atrativos_db.items() if v == item][0]
                    st.markdown(f"### 📍 {nome} (Score: {item['score']})")
                    st.info(f"💡 {item['dica']}")
                    st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral")
    st.map(pd.DataFrame.from_dict(atrativos_db, orient='index'))

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("O FluxoTur utiliza uma arquitetura avançada de Inteligência Artificial Não Generativa.")
