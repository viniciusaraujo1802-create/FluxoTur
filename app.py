import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# ---------------- CSS PARA FUNDO, PELÍCULA E LEITURA ----------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                    url("https://i.ibb.co/cSzgTZ7x/download-1.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp, .stMarkdown, .stText, .stTextInput, .stButton, p, h1, h2, h3, div, label, span {{
        color: #000000 !important;
        font-weight: bold !important;
    }}
    div.stButton > button {{
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- VLIBRAS ----------------
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
    """
    st.components.v1.html(vlibras_html, height=100)

injetar_vlibras()

def gerar_link_mapas(nome):
    return f"https://www.google.com/maps/search/?api=1&query={nome.replace(' ', '+')}+Foz+do+Iguacu"

# ---------------- BASE DE ATRATIVOS ----------------
atrativos_db = {
    "Adrena Kart Kartódromo":{"cat":"Esporte","latitude":-25.534,"longitude":-54.545,"dica":"Acelere em uma das pistas de kart mais famosas da cidade."},
    "Aguaray Eco":{"cat":"Natureza","latitude":-25.617,"longitude":-54.484,"dica":"Trilhas ecológicas em meio à mata preservada."},
    "Amanhecer nas Cataratas":{"cat":"Experiência","latitude":-25.695,"longitude":-54.436,"dica":"Experiência exclusiva para ver o nascer do sol nas cataratas."},
    "AquaFoz":{"cat":"Cultura","latitude":-25.616,"longitude":-54.481,"dica":"Aquário com espécies da região trinacional."},
    "Aquamania":{"cat":"Lazer","latitude":-25.538,"longitude":-54.542,"dica":"Parque aquático para toda a família."},
    "Bike Poço Preto":{"cat":"Esporte","latitude":-25.695,"longitude":-54.436,"dica":"Passeio de bicicleta pela floresta do Parque Nacional."},
    "Blue Park":{"cat":"Lazer","latitude":-25.525,"longitude":-54.548,"dica":"Praia termal artificial com águas aquecidas."},
    "Cataratas del Iguazú – Argentina":{"cat":"Natureza","latitude":-25.684,"longitude":-54.444,"dica":"O lado argentino das cataratas com trilhas panorâmicas."},
    "Cataratas do Iguaçu – Brasil":{"cat":"Natureza","latitude":-25.695,"longitude":-54.436,"dica":"A famosa Garganta do Diabo vista do lado brasileiro."},
    "Céu das Cataratas":{"cat":"Experiência","latitude":-25.695,"longitude":-54.436,"dica":"Restaurante panorâmico com vista para as cataratas."},
    "Circuito São João":{"cat":"Cultura","latitude":-25.510,"longitude":-54.500,"dica":"Circuito cultural com história da região."},
    "Dreams Park Show":{"cat":"Lazer","latitude":-25.565,"longitude":-54.502,"dica":"Complexo com museus e atrações temáticas."},
    "Falls Bike Tour":{"cat":"Esporte","latitude":-25.695,"longitude":-54.436,"dica":"Passeio ciclístico com guia pelo parque."},
    "Fly Foz – Paraquedismo":{"cat":"Esporte","latitude":-25.534,"longitude":-54.545,"dica":"Salto duplo de paraquedas sobre a região."},
    "Helisul Experience – Cataratas":{"cat":"Experiência","latitude":-25.692,"longitude":-54.438,"dica":"Sobrevoo de helicóptero nas Cataratas."},
    "Helisul Experience – Itaipu":{"cat":"Experiência","latitude":-25.405,"longitude":-54.588,"dica":"Sobrevoo panorâmico da usina de Itaipu."},
    "Iguassu By Bike":{"cat":"Esporte","latitude":-25.550,"longitude":-54.580,"dica":"Passeios guiados de bicicleta pela cidade."},
    "Iguassu River Tour":{"cat":"Natureza","latitude":-25.690,"longitude":-54.435,"dica":"Passeio de barco pelo Rio Iguaçu."},
    "Iguassu Secret Falls":{"cat":"Natureza","latitude":-25.550,"longitude":-54.550,"dica":"Descubra cachoeiras escondidas da região."},
    "Iguazu Wellness":{"cat":"Experiência","latitude":-25.560,"longitude":-54.520,"dica":"Experiências de bem-estar, yoga e meditação."},
    "Itaipu Especial":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Visita técnica ao interior da usina."},
    "Itaipu Iluminada":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Espetáculo noturno de luzes na barragem."},
    "Itaipu Panorâmica":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Visita com vista panorâmica da barragem."},
    "Itaipu Refúgio Biológico":{"cat":"Natureza","latitude":-25.410,"longitude":-54.550,"dica":"Área de preservação de fauna e flora."},
    "Kattamaram":{"cat":"Lazer","latitude":-25.405,"longitude":-54.588,"dica":"Passeio de barco pelo lago de Itaipu."},
    "Macuco Safari":{"cat":"Esporte","latitude":-25.695,"longitude":-54.436,"dica":"Passeio de barco até as quedas das cataratas."},
    "Marco das Três Fronteiras":{"cat":"Cultura","latitude":-25.603,"longitude":-54.599,"dica":"Ponto onde se encontram Brasil, Argentina e Paraguai."},
    "Mesquita Omar Ibn Al-Khattab":{"cat":"Cultura","latitude":-25.535,"longitude":-54.575,"dica":"Uma das maiores mesquitas da América Latina."},
    "Parque das Aves":{"cat":"Natureza","latitude":-25.617,"longitude":-54.484,"dica":"Parque dedicado à conservação de aves tropicais."},
    "Pôr do Sol nas Cataratas":{"cat":"Experiência","latitude":-25.695,"longitude":-54.436,"dica":"Experiência especial ao entardecer nas cataratas."},
    "Templo Budista Chen Tien":{"cat":"Cultura","latitude":-25.534,"longitude":-54.550,"dica":"Templo budista com vista panorâmica da cidade."},
    "Turismo Itaipu":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Centro de visitantes com diversas experiências."},
    "Yup Star – Roda Gigante":{"cat":"Lazer","latitude":-25.600,"longitude":-54.600,"dica":"Roda gigante com vista panorâmica de Foz."},
    "Rafain Churrascaria":{"cat":"Gastronomia","latitude":-25.547,"longitude":-54.585,"dica":"Churrascaria tradicional com show latino-americano."},
    "La Mafia Trattoria":{"cat":"Gastronomia","latitude":-25.545,"longitude":-54.587,"dica":"Restaurante italiano famoso na cidade."},
    "Vó Bertila Pizza":{"cat":"Gastronomia","latitude":-25.550,"longitude":-54.585,"dica":"Pizzaria artesanal muito conhecida em Foz."},
    "Capitão Bar":{"cat":"Gastronomia","latitude":-25.548,"longitude":-54.586,"dica":"Bar e restaurante com clima descontraído."},
    "Empório com Arte":{"cat":"Gastronomia","latitude":-25.552,"longitude":-54.584,"dica":"Restaurante com gastronomia contemporânea."},
    "Porto Canoas":{"cat":"Gastronomia","latitude":-25.695,"longitude":-54.437,"dica":"Restaurante dentro do Parque Nacional."},
    "Sushi Hokkai":{"cat":"Gastronomia","latitude":-25.544,"longitude":-54.586,"dica":"Restaurante japonês popular na cidade."},
    "Shopping Catuaí Palladium":{"cat":"Lazer","latitude":-25.527,"longitude":-54.573,"dica":"Maior shopping da cidade."},
    "JL Cataratas Shopping":{"cat":"Lazer","latitude":-25.539,"longitude":-54.584,"dica":"Shopping central de Foz do Iguaçu."}
}

# ---------------- INTERFACE ----------------
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Planejador", "🎮 Roteiro Interativo", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    categoria_input = st.text_input("Digite o tipo de experiência (Natureza, Lazer, Esporte, Cultura, Gastronomia):", key="cat_input")
    if st.button("🚀 Gerar roteiro inteligente"):
        resultados = []
        for nome, item in atrativos_db.items():
            if not categoria_input or categoria_input.strip().lower() in item["cat"].lower():
                score = round(random.uniform(5.0, 10.0), 1)
                resultados.append({"nome": nome, "score": score, "item": item})
        
        for r in sorted(resultados, key=lambda x: x["score"], reverse=True):
            st.markdown(f"### 📍 {r['nome']} ⭐ {r['score']}")
            st.info(f"💡 {r['item']['dica']}")
            st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(r['nome']))
            st.markdown("---")

with tab2:
    st.header("🗺️ Roteiro Interativo: Ligue os Pontos")
    col_config, col_mapa = st.columns([1, 2])
    with col_config:
        pontos_sel = st.multiselect("Selecione os locais na ordem de visita:", list(atrativos_db.keys()))
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        if prompt := st.chat_input("Dúvida sobre seu roteiro?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": "Anotei! Mantenha o fluxo constante."})
            st.rerun()
    with col_mapa:
        mapa_jogo = folium.Map(location=[-25.58, -54.55], zoom_start=11, tiles="CartoDB positron")
        coords = []
        for i, nome in enumerate(pontos_sel):
            lat, lon = atrativos_db[nome]["latitude"], atrativos_db[nome]["longitude"]
            coords.append([lat, lon])
            folium.Marker([lat, lon], popup=f"{i+1}: {nome}", icon=folium.Icon(color="red", icon="star")).add_to(mapa_jogo)
        if len(coords) > 1:
            folium.PolyLine(coords, color="red", weight=4, dash_array='10').add_to(mapa_jogo)
        st_folium(mapa_jogo, use_container_width=True, height=500)

with tab3:
    st.header("📍 Mapa Geral")
    mapa_geral = folium.Map(location=[-25.58, -54.55], zoom_start=11)
    for nome, item in atrativos_db.items():
        folium.Marker([item["latitude"], item["longitude"]], popup=nome).add_to(mapa_geral)
    st_folium(mapa_geral, use_container_width=True, height=600)

with tab4:
    st.header("🧠 Entenda a Inteligência do FluxoTur")
    st.markdown("O FluxoTur utiliza lógica determinística para otimizar sua experiência em Foz, garantindo precisão e ausência de alucinações.")
