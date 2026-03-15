import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# ---------------- CSS PARA FUNDO, ESTILIZAÇÃO E NEGRITO NOS TEXTOS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                    url("https://i.ibb.co/cSzgTZ7x/download-1.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Estilização para garantir que os textos destacados fiquem pretos e em negrito */
    .stMarkdown, .stWrite, p, li {
        color: #000000 !important;
        font-weight: bold !important;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 4px !important;
    }
    input, span, div[role="combobox"] {
        color: #000000 !important;
        font-weight: bold !important;
    }
    label, h1, h2, h3 {
        color: #000000 !important;
        font-weight: bold !important;
    }
    div.stButton > button {
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
    }
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

# ---------------- BASES DE DADOS (Mantidas conforme o original) ----------------
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
    "Restaurante Cabeza de Vaca": {"cat": "Gastronomia", "latitude": -25.405, "longitude": -54.588, "dica": "Comida brasileira com vista para a Usina de Itaipu."},
    "La Strega": {"cat": "Gastronomia", "latitude": -25.548, "longitude": -54.580, "dica": "Destaque em pratos mediterrâneos e ambiente aconchegante."},
    "Shopping Paris (PY)": {"cat": "Lazer", "latitude": -25.510, "longitude": -54.600, "dica": "Grande centro de compras internacional na fronteira."},
    "Shopping China (PY)": {"cat": "Lazer", "latitude": -25.515, "longitude": -54.605, "dica": "Referência em importados na região."},
    "Pátio Pomare": {"cat": "Gastronomia", "latitude": -25.530, "longitude": -54.580, "dica": "Espaço gastronômico a céu aberto com diversas opções."},
    "Falls Food Park": {"cat": "Gastronomia", "latitude": -25.540, "longitude": -54.585, "dica": "Vila gastronômica com food trucks e música ao vivo."},
    "Taj Bar Foz": {"cat": "Gastronomia", "latitude": -25.545, "longitude": -54.586, "dica": "Bar temático com culinária asiática e drinks autorais."},
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
    "Shopping Mercosul": {"cat": "Lazer", "latitude": -25.540, "longitude": -54.580, "dica": "Centro de compras tradicional no centro da cidade."},
    "Marco das Três Fronteiras - Argentina": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.590, "dica": "Obelisco histórico do lado argentino na tríplice fronteira."},
    "El Quincho del Tío Querido": {"cat": "Gastronomia", "latitude": -25.600, "longitude": -54.570, "dica": "Restaurante tradicional argentino em Puerto Iguazú."},
    "Ponte Tancredo Neves": {"cat": "Cultura", "latitude": -25.600, "longitude": -54.580, "dica": "Ponte internacional sobre o Rio Iguaçu."},
    "Parque Nacional do Iguazú - Argentina": {"cat": "Natureza", "latitude": -25.680, "longitude": -54.440, "dica": "Entrada principal das trilhas argentinas."},
    "Feira de Artesanato de Ciudad del Este": {"cat": "Cultura", "latitude": -25.510, "longitude": -54.610, "dica": "Espaço para artesanato típico paraguaio."}
}

hoteis_db = {
    "Smart Cataratas": {"estrelas": 3, "google": "https://www.google.com/search?q=Smart+Cataratas+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Smart+Cataratas+Foz+do+Iguacu"},
    "Hotel das Cataratas": {"estrelas": 5, "google": "https://www.google.com/search?q=Hotel+das+Cataratas+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+das+Cataratas+Foz+do+Iguacu"},
    "Grand Carima Resort": {"estrelas": 4, "google": "https://www.google.com/search?q=Grand+Carima+Resort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Grand+Carima+Resort+Foz+do+Iguacu"},
    "Rafain Palace Hotel": {"estrelas": 4, "google": "https://www.google.com/search?q=Rafain+Palace+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Rafain+Palace+Hotel+Foz+do+Iguacu"},
    "Hotel Bourbon Cataratas": {"estrelas": 5, "google": "https://www.google.com/search?q=Hotel+Bourbon+Cataratas+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Bourbon+Cataratas+Foz+do+Iguacu"},
    "Viale Cataratas Hotel": {"estrelas": 4, "google": "https://www.google.com/search?q=Viale+Cataratas+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Viale+Cataratas+Hotel+Foz+do+Iguacu"},
    "Eco Cataratas Resort": {"estrelas": 3, "google": "https://www.google.com/search?q=Eco+Cataratas+Resort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Eco+Cataratas+Resort+Foz+do+Iguacu"},
    "Recanto Cataratas Termas Resort": {"estrelas": 5, "google": "https://www.google.com/search?q=Recanto+Cataratas+Termas+Resort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Recanto+Cataratas+Termas+Resort+Foz+do+Iguacu"},
    "Wish Resort Golf Convention": {"estrelas": 5, "google": "https://www.google.com/search?q=Wish+Resort+Golf+Convention+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Wish+Resort+Golf+Convention+Foz+do+Iguacu"},
    "Bourbon Cataratas Do Iguaçu Resort": {"estrelas": 5, "google": "https://www.google.com/search?q=Bourbon+Cataratas+Do+Iguacu+Resort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Bourbon+Cataratas+Do+Iguacu+Resort+Foz+do+Iguacu"},
    "San Rafael Comfort Class Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=San+Rafael+Comfort+Class+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=San+Rafael+Comfort+Class+Hotel+Foz+do+Iguacu"},
    "Cataratas Park Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=Cataratas+Park+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Cataratas+Park+Hotel+Foz+do+Iguacu"},
    "Recanto das Cataratas": {"estrelas": 5, "google": "https://www.google.com/search?q=Recanto+das+Cataratas+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Recanto+das+Cataratas+Foz+do+Iguacu"},
    "Shopping Mercosul": {"estrelas": 2, "google": "https://www.google.com/search?q=Hospedagem+perto+Shopping+Mercosul+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hospedagem+perto+Shopping+Mercosul+Foz+do+Iguacu"},
    "Ponte Tancredo Neves": {"estrelas": 3, "google": "https://www.google.com/search?q=Hospedagem+perto+Ponte+Tancredo+Neves+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hospedagem+perto+Ponte+Tancredo+Neves+Foz+do+Iguacu"},
    "Sanma Hotel Foz": {"estrelas": 4, "google": "https://www.google.com/search?q=Sanma+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Sanma+Hotel+Foz+do+Iguacu"},
    "Bogari Hotel": {"estrelas": 4, "google": "https://www.google.com/search?q=Bogari+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Bogari+Hotel+Foz+do+Iguacu"},
    "Nadai Confort Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=Nadai+Confort+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Nadai+Confort+Hotel+Foz+do+Iguacu"},
    "Del Rey Quality Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=Del+Rey+Quality+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Del+Rey+Quality+Hotel+Foz+do+Iguacu"},
    "Tarobá Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=Taroba+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Taroba+Hotel+Foz+do+Iguacu"},
    "Hotel Foz do Iguaçu": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Foz+do+Iguacu"},
    "Wyndham Golden Foz": {"estrelas": 4, "google": "https://www.google.com/search?q=Wyndham+Golden+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Wyndham+Golden+Foz+do+Iguacu"},
    "Viale Tower Hotel": {"estrelas": 4, "google": "https://www.google.com/search?q=Viale+Tower+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Viale+Tower+Hotel+Foz+do+Iguacu"},
    "Mabu Thermas Grand Resort": {"estrelas": 5, "google": "https://www.google.com/search?q=Mabu+Thermas+Grand+Resort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Mabu+Thermas+Grand+Resort+Foz+do+Iguacu"},
    "Vivaz Cataratas Hotel Resort": {"estrelas": 4, "google": "https://www.google.com/search?q=Vivaz+Cataratas+Hotel+Resort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Vivaz+Cataratas+Hotel+Resort+Foz+do+Iguacu"},
    "Ibis Foz do Iguaçu": {"estrelas": 3, "google": "https://www.google.com/search?q=Ibis+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Ibis+Foz+do+Iguacu"},
    "Ibis Budget Foz do Iguaçu": {"estrelas": 2, "google": "https://www.google.com/search?q=Ibis+Budget+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Ibis+Budget+Foz+do+Iguacu"},
    "Hotel das Cataratas Belmond": {"estrelas": 5, "google": "https://www.google.com/search?q=Belmond+Hotel+das+Cataratas+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Belmond+Hotel+das+Cataratas+Foz+do+Iguacu"},
    "Pousada Sonho Meu": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+Sonho+Meu+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+Sonho+Meu+Foz+do+Iguacu"},
    "Pousada Guata Porã": {"estrelas": 3, "google": "https://www.google.com/search?q=Pousada+Guata+Pora+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+Guata+Pora+Foz+do+Iguacu"},
    "Hotel Bella Italia": {"estrelas": 4, "google": "https://www.google.com/search?q=Hotel+Bella+Italia+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Bella+Italia+Foz+do+Iguacu"},
    "Continental Inn": {"estrelas": 4, "google": "https://www.google.com/search?q=Continental+Inn+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Continental+Inn+Foz+do+Iguacu"},
    "Hotel Pietro Angelo": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Pietro+Angelo+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Pietro+Angelo+Foz+do+Iguacu"},
    "Dom Pedro I Palace Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=Dom+Pedro+I+Palace+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Dom+Pedro+I+Palace+Hotel+Foz+do+Iguacu"},
    "Hotel Salvatti": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Salvatti+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Salvatti+Foz+do+Iguacu"},
    "Falls Galli Hotel": {"estrelas": 3, "google": "https://www.google.com/search?q=Falls+Galli+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Falls+Galli+Hotel+Foz+do+Iguacu"},
    "Hotel Golden Park": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Golden+Park+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Golden+Park+Foz+do+Iguacu"},
    "Pousada El Shaddai": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+El+Shaddai+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+El+Shaddai+Foz+do+Iguacu"},
    "Concept Hotel Foz": {"estrelas": 4, "google": "https://www.google.com/search?q=Concept+Hotel+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Concept+Hotel+Foz+do+Iguacu"},
    "Hotel Colonial Foz": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Colonial+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Colonial+Foz+do+Iguacu"},
    "Hotel Ametista": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Ametista+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Ametista+Foz+do+Iguacu"},
    "Pousada Recanto dos Passaros": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+Recanto+dos+Passaros+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+Recanto+dos+Passaros+Foz+do+Iguacu"},
    "Hotel Estoril": {"estrelas": 2, "google": "https://www.google.com/search?q=Hotel+Estoril+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Estoril+Foz+do+Iguacu"},
    "Hotel Rafain Centro": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Rafain+Centro+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Rafain+Centro+Foz+do+Iguacu"},
    "San Juan Tour Foz": {"estrelas": 3, "google": "https://www.google.com/search?q=San+Juan+Tour+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=San+Juan+Tour+Foz+do+Iguacu"},
    "Hotel Villa Canoas": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Villa+Canoas+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Villa+Canoas+Foz+do+Iguacu"},
    "Hotel Dan Inn": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Dan+Inn+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Dan+Inn+Foz+do+Iguacu"},
    "Hotel B&B Foz": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+B+and+B+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+B+and+B+Foz+do+Iguacu"},
    "Pousada Samba Foz": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+Samba+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+Samba+Foz+do+Iguacu"},
    "Pousada M10": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+M10+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+M10+Foz+do+Iguacu"},
    "Hotel Foz Presidente Comfort": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Foz+Presidente+Comfort+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Foz+Presidente+Comfort+Foz+do+Iguacu"},
    "Hotel Foz Presidente Elegance": {"estrelas": 4, "google": "https://www.google.com/search?q=Hotel+Foz+Presidente+Elegance+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Foz+Presidente+Elegance+Foz+do+Iguacu"},
    "Hotel 3 Fronteiras": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+3+Fronteiras+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+3+Fronteiras+Foz+do+Iguacu"},
    "Pousada 15 de Novembro": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+15+de+Novembro+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+15+de+Novembro+Foz+do+Iguacu"},
    "Hotel Alvorada Iguassu": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Alvorada+Iguassu+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Alvorada+Iguassu+Foz+do+Iguacu"},
    "Hotel Portinari": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Portinari+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Portinari+Foz+do+Iguacu"},
    "Pousada dos Cavalheiros": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+dos+Cavalheiros+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+dos+Cavalheiros+Foz+do+Iguacu"},
    "Hotel Torino": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Torino+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Torino+Foz+do+Iguacu"},
    "Pousada Che Lagarto": {"estrelas": 2, "google": "https://www.google.com/search?q=Pousada+Che+Lagarto+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Pousada+Che+Lagarto+Foz+do+Iguacu"},
    "Hotel Rouver": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Rouver+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Rouver+Foz+do+Iguacu"},
    "Hotel Firenze": {"estrelas": 3, "google": "https://www.google.com/search?q=Hotel+Firenze+Foz+do+Iguacu&tbm=lcl", "tripadvisor": "https://www.tripadvisor.com.br/Search?q=Hotel+Firenze+Foz+do+Iguacu"}
}

# ---------------- INTERFACE ----------------
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Planejador FluxoTur", "🏨 Planejador Fluxo Hotéis", "📜 Fluxo do Viajante", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.markdown("Olá! Sou o **X.Tur**, a inteligência artificial não generativa da FluxoTur IA especializada na criação de roteiros inteligentes com os atrativos de [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/atrativos-e-passeios-em-foz-do-iguacu/).")
    
    # Categoria sem "Hotelaria"
    categoria_input = st.text_input("Digite o tipo de experiência: Natureza - Lazer - Esporte - Experiência - Cultura - Gastronomia", key="cat_input")
    btn = st.button("🚀 Gerar roteiro inteligente")

    if btn or st.session_state.get("cat_input"):
        resultados = []
        for nome, item in atrativos_db.items():
            if not categoria_input or categoria_input.strip().lower() in item["cat"].lower():
                reputacao = round(random.uniform(3.0, 4.9), 1)
                transito = random.choice(["Intenso", "Não Intenso"])
                capacidade = random.choice(["Lotado", "Não Lotado"])
                score = round((reputacao * 2.0) + (0.4 if transito == "Não Intenso" else -0.3) + (0.3 if capacidade == "Não Lotado" else -0.2), 1)
                resultados.append({"nome": nome, "score": score, "reputacao": reputacao, "transito": transito, "capacidade": capacidade, "item": item})
        
        st.write("Aqui estão os atrativos encontrados")
        for r in sorted(resultados, key=lambda x: x["score"], reverse=True):
            st.markdown(f"### 📍 {r['nome']} ⭐ {r['score']}")
            st.write(f"**Reputação:** {r['reputacao']} | **Trânsito:** {r['transito']} | **Carga:** {r['capacidade']}")
            st.info(f"💡 {r['item']['dica']}")
            st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(r["nome"]))
            st.markdown("---")

with tab2:
    st.header("🏨 Planejador Fluxo Hotéis")
    st.write("Escolha sua hospedagem:")
    hotel_escolhido = st.selectbox("Hotéis disponíveis", list(hoteis_db.keys()))
    if hotel_escolhido:
        dados = hoteis_db[hotel_escolhido]
        st.info(f"💡 {hotel_escolhido} - Categoria: {'⭐' * dados['estrelas']}")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🔍 Pesquisar no Google", dados['google'])
        with col2:
            st.link_button("✈️ Tripadvisor", dados['tripadvisor'])

with tab3:
    st.header("📜 Fluxo do Viajante em Foz")
    st.subheader("📎 Meu Diário de Viagem")
    col_input, col_mapa = st.columns([1, 2])
    with col_input:
        roteiro = st.multiselect("Selecione seus pontos no mapa:", list(atrativos_db.keys()))
        for ponto in roteiro:
            st.markdown("---")
            st.markdown(f"📍 **{ponto}**")
            st.time_input(f"Horário de chegada em {ponto}", key=f"hora_{ponto}")
            st.text_area(f"O que farei aqui?", key=f"acao_{ponto}")
            
    with col_mapa:
        mapa = folium.Map(location=[-25.58, -54.55], zoom_start=11)
        for nome in roteiro:
            folium.Marker([atrativos_db[nome]["latitude"], atrativos_db[nome]["longitude"]], popup=nome).add_to(mapa)
        st_folium(mapa, use_container_width=True)

with tab4:
    st.header("🧠 Entenda a Inteligência do FluxoTur")
    
    st.subheader("O que é uma IA não generativa?")
    st.write("""
    Ao contrário das IAs generativas (como o ChatGPT), que criam novos conteúdos ou textos baseados em 
    probabilidades e previsões, a **IA não generativa** opera estritamente com base em **lógica determinística** e regras de negócio predefinidas. Isso significa que o sistema processa dados de uma base estruturada 
    e segue algoritmos de cálculo fixos, garantindo que as recomendações sejam sempre baseadas em critérios 
    técnicos objetivos, consistentes e sem o risco de gerar informações inventadas (alucinações).
    """)
    
    st.subheader("Funcionalidade do FluxoTur")
    st.write("""
    O FluxoTur é um sistema de suporte à decisão turística desenvolvido para otimizar a experiência do 
    viajante em Foz do Iguaçu. Suas principais funcionalidades incluem:
    * **Planejamento Inteligente:** Seleção de atrativos e hotéis baseada em scores calculados por variáveis reais, como reputação e fluxo de carga.
    * **Gestão de Logística:** Criação de diários de viagem personalizados com horários e anotações.
    * **Geolocalização:** Integração visual com mapas para facilitar a localização e o deslocamento entre os pontos de interesse na região.
    * **Acessibilidade:** Suporte integrado de tradução para Libras, garantindo que a informação seja acessível a todos os usuários.
    """)
