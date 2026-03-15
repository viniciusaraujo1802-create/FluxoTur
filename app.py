Aqui está o código completo, com a base de dados atualizada contendo todos os novos atrativos incluídos, preservando integralmente a estrutura e a lógica anteriores.

```python
import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# ---------------- CSS PARA FUNDO E ESTILIZAÇÃO DOS INPUTS ----------------
st.markdown(
    """
    <style>
    /* 1. Design Geral do Fundo */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                    url("https://i.ibb.co/cSzgTZ7x/download-1.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* 2. Forçar todos os inputs (text_input e multiselect) para o seu padrão: Fundo branco, borda preta */
    div[data-baseweb="input"], 
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 4px !important;
    }

    /* 3. Garantir texto preto dentro dos campos */
    input, span, div[role="combobox"] {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* 4. Cor do texto dos rótulos (labels) */
    label, h1, h2, h3, p {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* 5. Estilo do Botão */
    div.stButton > button {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
    }
    
    /* 6. Estilo específico do mapa (Sépia) */
    .stFolium {
        filter: sepia(90%) hue-rotate(350deg) brightness(95%);
        border: 4px solid #4E342E;
    }
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
  "Adrena Kart Kartódromo": {"cat": "Esporte", "latitude": -25.534, "longitude": -54.545, "dica": "Acelere em uma das pistas de kart mais famosas da cidade."},
  "Aguaray Eco": {"cat": "Natureza", "latitude": -25.617, "longitude": -54.484, "dica": "Trilhas ecológicas em meio à mata preservada."},
  "Amanhecer nas Cataratas": {"cat": "Experiência", "latitude": -25.695, "longitude": -54.436, "dica": "Experiência exclusiva para ver o nascer do sol nas cataratas."},
  "AquaFoz": {"cat": "Cultura", "latitude": -25.616, "longitude": -54.481, "dica": "Aquário com espécies da região trinacional."},
  "Aquamania": {"cat": "Lazer", "latitude": -25.538, "longitude": -54.542, "dica": "Parque aquático para toda a família."},
  "Bike Poço Preto": {"cat": "Esporte", "latitude": -25.695, "longitude": -54.436, "dica": "Passeio de bicicleta pela floresta do Parque Nacional."},
  "Blue Park": {"cat": "Lazer", "latitude": -25.525, "longitude": -54.548, "dica": "Praia termal artificial com águas aquecidas."},
  "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "latitude": -25.684, "longitude": -54.444, "dica": "O lado argentino das cataratas com trilhas panorâmicas."},
  "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "latitude": -25.695, "longitude": -54.436, "dica": "A famosa Garganta do Diabo vista do lado brasileiro."},
  "Céu das Cataratas": {"cat": "Experiência", "latitude": -25.695, "longitude": -54.436, "dica": "Restaurante panorâmico com vista para as cataratas."},
  "Circuito São João": {"cat": "Cultura", "latitude": -25.510, "longitude": -54.500, "dica": "Circuito cultural com história da região."},
  "Dreams Park Show": {"cat": "Lazer", "latitude": -25.565, "longitude": -54.502, "dica": "Complexo com museus e atrações temáticas."},
  "Falls Bike Tour": {"cat": "Esporte", "latitude": -25.695, "longitude": -54.436, "dica": "Passeio ciclístico com guia pelo parque."},
  "Fly Foz – Paraquedismo": {"cat": "Esporte", "latitude": -25.534, "longitude": -54.545, "dica": "Salto duplo de paraquedas sobre a região."},
  "Helisul Experience – Cataratas": {"cat": "Experiência", "latitude": -25.692, "longitude": -54.438, "dica": "Sobrevoo de helicóptero nas Cataratas."},
  "Helisul Experience – Itaipu": {"cat": "Experiência", "latitude": -25.405, "longitude": -54.588, "dica": "Sobrevoo panorâmico da usina de Itaipu."},
  "Iguassu By Bike": {"cat": "Esporte", "latitude": -25.550, "longitude": -54.580, "dica": "Passeios guiados de bicicleta pela cidade."},
  "Iguassu River Tour": {"cat": "Natureza", "latitude": -25.690, "longitude": -54.435, "dica": "Passeio de barco pelo Rio Iguaçu."},
  "Iguassu Secret Falls": {"cat": "Natureza", "latitude": -25.550, "longitude": -54.550, "dica": "Descubra cachoeiras escondidas da região."},
  "Iguazu Wellness": {"cat": "Experiência", "latitude": -25.560, "longitude": -54.520, "dica": "Experiências de bem-estar, yoga e meditação."},
  "Itaipu Especial": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "Visita técnica ao interior da usina."},
  "Itaipu Iluminada": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "Espetáculo noturno de luzes na barragem."},
  "Itaipu Panorâmica": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "Visita com vista panorâmica da barragem."},
  "Itaipu Refúgio Biológico": {"cat": "Natureza", "latitude": -25.410, "longitude": -54.550, "dica": "Área de preservação de fauna e flora."},
  "Kattamaram": {"cat": "Lazer", "latitude": -25.405, "longitude": -54.588, "dica": "Passeio de barco pelo lago de Itaipu."},
  "Macuco Safari": {"cat": "Esporte", "latitude": -25.695, "longitude": -54.436, "dica": "Passeio de barco até as quedas das cataratas."},
  "Marco das Três Fronteiras": {"cat": "Cultura", "latitude": -25.603, "longitude": -54.599, "dica": "Ponto onde se encontram Brasil, Argentina e Paraguai."},
  "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "latitude": -25.535, "longitude": -54.575, "dica": "Uma das maiores mesquitas da América Latina."},
  "Parque das Aves": {"cat": "Natureza", "latitude": -25.617, "longitude": -54.484, "dica": "Parque dedicado à conservação de aves tropicais."},
  "Pôr do Sol nas Cataratas": {"cat": "Experiência", "latitude": -25.695, "longitude": -54.436, "dica": "Experiência especial ao entardecer nas cataratas."},
  "Templo Budista Chen Tien": {"cat": "Cultura", "latitude": -25.534, "longitude": -54.550, "dica": "Templo budista com vista panorâmica da cidade."},
  "Turismo Itaipu": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "Centro de visitantes com diversas experiências."},
  "Yup Star – Roda Gigante": {"cat": "Lazer", "latitude": -25.600, "longitude": -54.600, "dica": "Roda gigante com vista panorâmica de Foz."},
  "Rafain Churrascaria": {"cat": "Gastronomia", "latitude": -25.547, "longitude": -54.585, "dica": "Churrascaria tradicional com show latino-americano."},
  "La Mafia Trattoria": {"cat": "Gastronomia", "latitude": -25.545, "longitude": -54.587, "dica": "Restaurante italiano famoso na cidade."},
  "Vó Bertila Pizza": {"cat": "Gastronomia", "latitude": -25.550, "longitude": -54.585, "dica": "Pizzaria artesanal muito conhecida em Foz."},
  "Capitão Bar": {"cat": "Gastronomia", "latitude": -25.548, "longitude": -54.586, "dica": "Bar e restaurante com clima descontraído."},
  "Empório com Arte": {"cat": "Gastronomia", "latitude": -25.552, "longitude": -54.584, "dica": "Restaurante com gastronomia contemporânea."},
  "Porto Canoas": {"cat": "Gastronomia", "latitude": -25.695, "longitude": -54.437, "dica": "Restaurante dentro do Parque Nacional."},
  "Sushi Hokkai": {"cat": "Gastronomia", "latitude": -25.544, "longitude": -54.586, "dica": "Restaurante japonês popular na cidade."},
  "Shopping Catuaí Palladium": {"cat": "Lazer", "latitude": -25.527, "longitude": -54.573, "dica": "Maior shopping da cidade."},
  "JL Cataratas Shopping": {"cat": "Lazer", "latitude": -25.539, "longitude": -54.584, "dica": "Shopping central de Foz do Iguaçu."},
  "277 CraftBeer": {"cat": "Gastronomia", "latitude": -25.540, "longitude": -54.580, "dica": "Cervejaria artesanal com rótulos locais e petiscos."},
  "Smart Cataratas": {"cat": "Hotelaria", "latitude": -25.545, "longitude": -54.570, "dica": "Hotel moderno com ótima localização para turistas."},
  "Hotel das Cataratas": {"cat": "Hotelaria", "latitude": -25.695, "longitude": -54.436, "dica": "Luxo e exclusividade dentro do Parque Nacional."},
  "Grand Carima Resort": {"cat": "Hotelaria", "latitude": -25.580, "longitude": -54.520, "dica": "Resort amplo com lazer completo para famílias."},
  "Rafain Palace Hotel": {"cat": "Hotelaria", "latitude": -25.550, "longitude": -54.560, "dica": "Tradicional centro de convenções e hospedagem."},
  "Restaurante Cabeza de Vaca": {"cat": "Gastronomia", "latitude": -25.405, "longitude": -54.588, "dica": "Comida brasileira com vista para a Usina de Itaipu."},
  "La Strega": {"cat": "Gastronomia", "latitude": -25.548, "longitude": -54.580, "dica": "Destaque em pratos mediterrâneos e ambiente aconchegante."},
  "Shopping Paris (PY)": {"cat": "Lazer", "latitude": -25.510, "longitude": -54.600, "dica": "Grande centro de compras internacional na fronteira."},
  "Shopping China (PY)": {"cat": "Lazer", "latitude": -25.515, "longitude": -54.605, "dica": "Referência em importados na região."},
  "Pátio Pomare": {"cat": "Gastronomia", "latitude": -25.530, "longitude": -54.580, "dica": "Espaço gastronômico a céu aberto com diversas opções."},
  "Falls Food Park": {"cat": "Gastronomia", "latitude": -25.540, "longitude": -54.585, "dica": "Vila gastronômica com food trucks e música ao vivo."},
  "Taj Bar Foz": {"cat": "Gastronomia", "latitude": -25.545, "longitude": -54.586, "dica": "Bar temático com culinária asiática e drinks autorais."},
  "Hotel Bourbon Cataratas": {"cat": "Hotelaria", "latitude": -25.550, "longitude": -54.550, "dica": "Resort completo focado em famílias e eventos."},
  "Viale Cataratas Hotel": {"cat": "Hotelaria", "latitude": -25.560, "longitude": -54.540, "dica": "Conforto e lazer próximo às principais vias de acesso."},
  "Eco Cataratas Resort": {"cat": "Hotelaria", "latitude": -25.570, "longitude": -54.530, "dica": "Opção de hospedagem integrada com a natureza."},
  "Opy – Experiência Indígena": {"cat": "Cultura", "latitude": -25.620, "longitude": -54.480, "dica": "Vivência cultural na aldeia Tekoa Mirim."},
  "Trilha do Bananeiras": {"cat": "Natureza", "latitude": -25.690, "longitude": -54.440, "dica": "Passeio em trilha suspensa com foco em observação de aves."},
  "Espaço das Américas": {"cat": "Lazer", "latitude": -25.555, "longitude": -54.575, "dica": "Local para shows e eventos de grande porte em Foz."},
  "Dreams Museu de Cera": {"cat": "Lazer", "latitude": -25.565, "longitude": -54.502, "dica": "Esculturas em cera de personalidades mundiais."},
  "Maravilhas do Mundo": {"cat": "Cultura", "latitude": -25.565, "longitude": -54.502, "dica": "Réplicas de monumentos famosos em miniatura."},
  "Dreams Ice Bar": {"cat": "Lazer", "latitude": -25.565, "longitude": -54.502, "dica": "Bar temático inteiramente construído em gelo."},
  "Dreams Motor Show": {"cat": "Lazer", "latitude": -25.565, "longitude": -54.502, "dica": "Museu de motocicletas clássicas com restaurante."},
  "Vale dos Dinossauros": {"cat": "Lazer", "latitude": -25.565, "longitude": -54.502, "dica": "Parque com réplicas animadas de dinossauros."},
  "Dino Adventure": {"cat": "Esporte", "latitude": -25.565, "longitude": -54.502, "dica": "Circuito de arvorismo e trilhas de aventura."},
  "Centro de Falcoaria": {"cat": "Natureza", "latitude": -25.565, "longitude": -54.502, "dica": "Espaço de reabilitação e voo de aves de rapina."},
  "Movie Cars": {"cat": "Lazer", "latitude": -25.600, "longitude": -54.580, "dica": "Atração focada em carros icônicos do cinema."},
  "Big Land": {"cat": "Lazer", "latitude": -25.600, "longitude": -54.580, "dica": "Parque onde você se sente pequeno em um mundo gigante."},
  "Show das Águas": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.580, "dica": "Espetáculo noturno de luzes, música e águas dançantes."},
  "Lumina Park": {"cat": "Lazer", "latitude": -25.600, "longitude": -54.580, "dica": "Parque iluminado com esculturas temáticas noturnas."},
  "Polo Astronômico de Itaipu": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "Observatório astronômico e planetário no complexo de Itaipu."},
  "Itaipu Ecomuseu": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "Museu que conta a história da construção da usina."},
  "Recanto Cataratas Termas Resort": {"cat": "Hotelaria", "latitude": -25.530, "longitude": -54.580, "dica": "Resort com piscinas termais e lazer completo."},
  "Wish Resort Golf Convention": {"cat": "Hotelaria", "latitude": -25.580, "longitude": -54.550, "dica": "Resort de luxo com campo de golfe próprio."},
  "Bourbon Cataratas Do Iguaçu Resort": {"cat": "Hotelaria", "latitude": -25.550, "longitude": -54.550, "dica": "Resort consagrado para famílias em Foz."},
  "San Rafael Comfort Class Hotel": {"cat": "Hotelaria", "latitude": -25.540, "longitude": -54.580, "dica": "Opção de hospedagem com bom custo-benefício."},
  "Cataratas Park Hotel": {"cat": "Hotelaria", "latitude": -25.550, "longitude": -54.570, "dica": "Hotel voltado para eventos e grupos turísticos."},
  "Zeppelin Old Bar": {"cat": "Gastronomia", "latitude": -25.545, "longitude": -54.585, "dica": "Bar temático famoso pelo rock and roll e lanches."},
  "Kings Pub": {"cat": "Gastronomia", "latitude": -25.548, "longitude": -54.586, "dica": "Pub com música ao vivo e variedade de chopes."},
  "Madero Tango (Argentina)": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.550, "dica": "Show de tango clássico com jantar em Puerto Iguazú."},
  "Cassino Iguazú (Argentina)": {"cat": "Lazer", "latitude": -25.605, "longitude": -54.555, "dica": "Cassino tradicional na fronteira argentina."},
  "Casino Acaray (Paraguai)": {"cat": "Lazer", "latitude": -25.510, "longitude": -54.610, "dica": "Opção de cassino e lazer em Ciudad del Este."},
  "Feirinha de Puerto Iguazú": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.550, "dica": "Feira tradicional com produtos típicos argentinos."},
  "La Aripuca": {"cat": "Cultura", "latitude": -25.610, "longitude": -54.550, "dica": "Monumento ecológico feito com madeiras resgatadas."},
  "Duty Free Shopping (Argentina)": {"cat": "Lazer", "latitude": -25.610, "longitude": -54.550, "dica": "Centro de compras de importados na fronteira."},
  "Mercado Público Barrageiro": {"cat": "Gastronomia", "latitude": -25.540, "longitude": -54.580, "dica": "Espaço com produtos coloniais e gastronomia local."},
  "Catedral Nossa Senhora de Guadalupe": {"cat": "Cultura", "latitude": -25.545, "longitude": -54.580, "dica": "Igreja de arquitetura marcante no centro de Foz."},
  "Praça da Paz": {"cat": "Lazer", "latitude": -25.540, "longitude": -54.580, "dica": "Principal praça central para eventos e caminhadas."},
  "Avenida Brasil": {"cat": "Cultura", "latitude": -25.545, "longitude": -54.580, "dica": "Rua central vibrante com comércio e gastronomia."},
  "Ponte da Integração": {"cat": "Cultura", "latitude": -25.500, "longitude": -54.600, "dica": "Nova ponte que liga Brasil e Paraguai."},
  "Ponte da Amizade": {"cat": "Cultura", "latitude": -25.510, "longitude": -54.610, "dica": "Ponte histórica que liga Foz a Ciudad del Este."},
  "Iporã Lenda Show": {"cat": "Cultura", "latitude": -25.560, "longitude": -54.550, "dica": "Espetáculo que conta lendas da região."},
  "Eco Park Foz": {"cat": "Natureza", "latitude": -25.565, "longitude": -54.500, "dica": "Abrigo de animais e apresentações de aves de rapina."},
  "Gramadão da Vila A": {"cat": "Lazer", "latitude": -25.450, "longitude": -54.550, "dica": "Espaço de lazer ao ar livre, ideal para piqueniques."},
  "Rua Pedro Basso": {"cat": "Lazer", "latitude": -25.550, "longitude": -54.580, "dica": "Conhecida como a rua mais bonita de Foz do Iguaçu."},
  "Cascata do Rio Monday (Paraguai)": {"cat": "Natureza", "latitude": -25.500, "longitude": -54.650, "dica": "Cachoeira impressionante próxima à fronteira."},
  "Pirá de Foz": {"cat": "Gastronomia", "latitude": -25.540, "longitude": -54.580, "dica": "Restaurante especializado em peixes de água doce."},
  "Shawarma do Alemão": {"cat": "Gastronomia", "latitude": -25.545, "longitude": -54.580, "dica": "Ponto tradicional para comer um autêntico shawarma."},
  "Costelão ao Fogo de Chão": {"cat": "Gastronomia", "latitude": -25.550, "longitude": -54.570, "dica": "Experiência gastronômica tradicional do sul do Brasil."},
  "Entrevero de Pinhão": {"cat": "Gastronomia", "latitude": -25.550, "longitude": -54.570, "dica": "Prato regional servido em diversos restaurantes locais."},
  "Refúgio Biológico Bela Vista": {"cat": "Natureza", "latitude": -25.410, "longitude": -54.550, "dica": "Área ambiental protegida dentro da usina de Itaipu."},
  "Recanto das Cataratas": {"cat": "Hotelaria", "latitude": -25.530, "longitude": -54.580, "dica": "Resort com piscinas termais e infraestrutura completa."},
  "Shopping Mercosul": {"cat": "Lazer", "latitude": -25.540, "longitude": -54.580, "dica": "Centro de compras tradicional no centro da cidade."},
  "Marco das Três Fronteiras - Argentina": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.590, "dica": "Obelisco histórico do lado argentino na tríplice fronteira."},
  "El Quincho del Tío Querido": {"cat": "Gastronomia", "latitude": -25.600, "longitude": -54.570, "dica": "Restaurante tradicional argentino em Puerto Iguazú."},
  "Ponte Tancredo Neves": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.580, "dica": "Ponte internacional sobre o Rio Iguaçu."},
  "Parque Nacional do Iguazú - Argentina": {"cat": "Natureza", "latitude": -25.680, "longitude": -54.440, "dica": "Entrada principal das trilhas argentinas."},
  "Feira de Artesanato de Ciudad del Este": {"cat": "Cultura", "latitude": -25.510, "longitude": -54.610, "dica": "Espaço para artesanato típico paraguaio."}
}

# ---------------- INTERFACE ----------------
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📜 Fluxo do Viajante", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.markdown("""
    Olá! Sou o **X.Tur**, a inteligência artificial não generativa da FluxoTur IA especializada na criação de roteiros inteligentes com os atrativos de [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/atrativos-e-passeios-em-foz-do-iguacu/).
    """)

    categoria_input = st.text_input(
        "Digite o tipo de experiência: Natureza - Lazer - Esporte - Experiência - Cultura - Gastronomia - Hotelaria",
        key="cat_input"
    )

    btn = st.button("🚀 Gerar roteiro inteligente")

    if btn or st.session_state.get("cat_input"):
        resultados = []
        for nome, item in atrativos_db.items():
            if not categoria_input or categoria_input.strip().lower() in item["cat"].lower():
                reputacao = round(random.uniform(3.0, 4.9), 1)
                transito = random.choice(["Intenso", "Não Intenso"])
                capacidade = random.choice(["Lotado", "Não Lotado"])
                
                score_bruto = (reputacao * 2.0)
                score_bruto += 1.0 if transito == "Não Intenso" else -1.0
                score_bruto += 1.0 if capacidade == "Não Lotado" else -1.0

                min_alvo, max_alvo = 5.3, 10.5
                min_atual, max_atual = 4.0, 11.8
                score_norm = min_alvo + ((score_bruto - min_atual) * (max_alvo - min_alvo) / (max_atual - min_atual))
                score = round(max(min_alvo, min(max_alvo, score_norm)), 1)

                resultados.append({
                    "nome": nome, "score": score, "reputacao": reputacao,
                    "transito": transito, "capacidade": capacidade, "item": item
                })

        resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)
        st.success(f"Aqui estão os {len(resultados)} locais encontrados")

        for r in resultados:
            st.markdown(f"### 📍 {r['nome']} ⭐ {r['score']}")
            st.write(f"**Reputação Digital:** {r['reputacao']} | **Fluxo de Trânsito:** {r['transito']} | **Capacidade de Carga:** {r['capacidade']}")
            st.info(f"💡 {r['item']['dica']}")
            st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(r["nome"]))
            st.markdown("---")

with tab2:
    st.header("📜 Fluxo do Viajante em Foz")
    
    col_input, col_mapa = st.columns([1, 2])

    with col_input:
        st.subheader("🎒 Meu Diário de Viagem")
        roteiro = st.multiselect("Selecione seus pontos no mapa:", list(atrativos_db.keys()))
        
        notas_roteiro = {}
        if roteiro:
            st.write("---")
            for local in roteiro:
                with st.expander(f"📍 {local}"):
                    hora = st.time_input(f"Horário de chegada em {local}", key=f"time_{local}")
                    atividade = st.text_area(f"O que farei aqui?", key=f"note_{local}")
                    notas_roteiro[local] = {"hora": hora, "atividade": atividade}

    with col_mapa:
        mapa_antigo = folium.Map(location=[-25.58, -54.55], zoom_start=11, tiles="OpenStreetMap")
        
        coords = []
        for i, nome in enumerate(roteiro):
            lat, lon = atrativos_db[nome]["latitude"], atrativos_db[nome]["longitude"]
            coords.append([lat, lon])
            
            folium.Marker(
                [lat, lon],
                popup=f"{i+1}: {nome}",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(mapa_antigo)
            
        if len(coords) > 1:
            folium.PolyLine(
                coords, 
                color="#4E342E", 
                weight=6, 
                opacity=0.8, 
                dash_array='10'
            ).add_to(mapa_antigo)
            
        st_folium(mapa_antigo, use_container_width=True, height=500)

with tab3:
    st.header("🧠 Entenda a Inteligência do FluxoTur")
    st.markdown("""
    O FluxoTur foi concebido como uma ferramenta de apoio à decisão turística em tempo real, utilizando uma lógica de otimização ponderada que vai além de uma simples lista de atrativos. Diferente de sistemas convencionais, nosso algoritmo processa informações estruturadas para calcular o Índice de Otimização da Experiência, um valor que reflete o equilíbrio ideal entre qualidade, agilidade e conforto. Ao priorizar locais com reputações digitais elevadas enquanto ponderamos as condições atuais de trânsito e a capacidade de carga dos espaços, transformamos dados brutos em uma recomendação personalizada que visa maximizar o seu aproveitamento em Foz do Iguaçu.
    """)
    st.markdown("""
    **Sobre a Inteligência Artificial Não Generativa:**
    Diferente dos modelos generativos que criam novos conteúdos ou textos baseados em probabilidades estatísticas, nossa IA não generativa atua com base em lógica determinística e regras estruturadas. Ela funciona processando dados reais e específicos em uma base de conhecimento curada, aplicando cálculos matemáticos precisos para classificar e recomendar atrativos. Em vez de imaginar uma resposta, o sistema avalia variáveis quantificáveis como reputação, fluxo e capacidade para entregar um resultado objetivo, consistente e livre de alucinações, garantindo que o roteiro sugerido seja sempre pautado na realidade atual dos pontos turísticos de Foz do Iguaçu.
    """)

```
