import streamlit as st
import random
import pandas as pd

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
        [vw] { position: fixed !important; bottom: 80px !important; right: 40px !important; z-index: 99999999 !important; }
    </style>
    """
    st.markdown(vlibras_html, unsafe_allow_html=True)

injetar_vlibras()

# --- BASE DE DADOS (33 ATRATIVOS COM LAT/LON) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "lat": -25.534, "lon": -54.545, "dica": "Prepare o capacete!"},
    "Aguaray Eco": {"cat": "Natureza", "lat": -25.617, "lon": -54.484, "dica": "Refúgio perfeito."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "lat": -25.695, "lon": -54.436, "dica": "Nascer do sol único."},
    "AquaFoz": {"cat": "Cultura", "lat": -25.616, "lon": -54.481, "dica": "Biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "lat": -25.538, "lon": -54.542, "dica": "Diversão em família."},
    "Bike Poço Preto": {"cat": "Esporte", "lat": -25.695, "lon": -54.436, "dica": "Pedale na floresta."},
    "Blue Park": {"cat": "Lazer", "lat": -25.525, "lon": -54.548, "dica": "Praia termal."},
    "Cataratas Argentina": {"cat": "Natureza", "lat": -25.684, "lon": -54.444, "dica": "Lado hermano."},
    "Cataratas Brasil": {"cat": "Natureza", "lat": -25.695, "lon": -54.436, "dica": "Garganta do Diabo."},
    "Céu das Cataratas": {"cat": "Experiência", "lat": -25.695, "lon": -54.436, "dica": "Sabor e vista."},
    "Circuito São João": {"cat": "Cultura", "lat": -25.510, "lon": -54.500, "dica": "Tradições."},
    "Dreams Park Show": {"cat": "Lazer", "lat": -25.565, "lon": -54.502, "dica": "Mundo mágico."},
    "Falls Bike Tour": {"cat": "Esporte", "lat": -25.695, "lon": -54.436, "dica": "Vento no rosto."},
    "Fly Foz": {"cat": "Esporte", "lat": -25.534, "lon": -54.545, "dica": "Paraquedismo."},
    "Helisul Experience": {"cat": "Experiência", "lat": -25.692, "lon": -54.438, "dica": "Foto aérea."},
    "Iguassu By Bike": {"cat": "Esporte", "lat": -25.550, "lon": -54.580, "dica": "Guias especializados."},
    "Iguassu River Tour": {"cat": "Natureza", "lat": -25.690, "lon": -54.435, "dica": "Perspectiva do rio."},
    "Iguassu Secret Falls": {"cat": "Natureza", "lat": -25.550, "lon": -54.550, "dica": "Cachoeiras ocultas."},
    "Iguazu Wellness": {"cat": "Experiência", "lat": -25.560, "lon": -54.520, "dica": "Bem-estar."},
    "Itaipu Especial": {"cat": "Cultura", "lat": -25.405, "lon": -54.588, "dica": "Visita técnica."},
    "Itaipu Iluminada": {"cat": "Cultura", "lat": -25.405, "lon": -54.588, "dica": "Show de luzes."},
    "Itaipu Panorâmica": {"cat": "Cultura", "lat": -25.405, "lon": -54.588, "dica": "Vista clássica."},
    "Itaipu Refúgio": {"cat": "Natureza", "lat": -25.410, "lon": -54.550, "dica": "Preservação."},
    "Kattamaram": {"cat": "Lazer", "lat": -25.405, "lon": -54.588, "dica": "No convés."},
    "Macuco Safari": {"cat": "Esporte", "lat": -25.695, "lon": -54.436, "dica": "Muita emoção."},
    "Marco das Fronteiras": {"cat": "Cultura", "lat": -25.603, "lon": -54.599, "dica": "Três países."},
    "Mesquita Omar": {"cat": "Cultura", "lat": -25.535, "lon": -54.575, "dica": "Arquitetura."},
    "Parque das Aves": {"cat": "Natureza", "lat": -25.617, "lon": -54.484, "dica": "Aves tropicais."},
    "Pôr do Sol Cataratas": {"cat": "Experiência", "lat": -25.695, "lon": -54.436, "dica": "Encerramento."},
    "Templo Budista": {"cat": "Cultura", "lat": -25.534, "lon": -54.550, "dica": "Paz interior."},
    "Turismo Itaipu": {"cat": "Cultura", "lat": -25.405, "lon": -54.588, "dica": "Segredos."},
    "Wonder Park Foz": {"cat": "Lazer", "lat": -25.550, "lon": -54.540, "dica": "Cinema."},
    "Yup Star": {"cat": "Lazer", "lat": -25.600, "lon": -54.600, "dica": "Roda Gigante."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador", "📍 Mapa", "🧠 Entenda"])
with tab1:
    pesquisa = st.text_input("O que deseja fazer?")
    if st.button("Gerar roteiro") or pesquisa:
        with st.spinner("Analisando..."):
            lista = [i for n, i in atrativos_db.items() if not pesquisa or i['cat'].lower() == pesquisa.lower()]
            for item in lista:
                nome = [k for k, v in atrativos_db.items() if v == item][0]
                st.markdown(f"### 📍 {nome} ({round(random.uniform(5.3, 10.5), 1)})")
                st.info(f"💡 {item['dica']}")
with tab2:
    st.map(pd.DataFrame.from_dict(atrativos_db, orient='index'))
