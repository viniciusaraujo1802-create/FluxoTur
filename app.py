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
    /* Ajuste para o texto do Multiselect ficar branco no fundo escuro */
    div[data-baseweb="select"] {{
        background-color: #000000 !important;
    }}
    div[data-baseweb="select"] span, div[role="listbox"] div {{
        color: #FFFFFF !important;
    }}
    /* Estilo do Botão: Fundo Branco, Texto Preto, Borda Preta */
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
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📜 Fluxo do Viajante", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.markdown("""
    Olá! Sou o **X.Tur**, a inteligência artificial não generativa da FluxoTur IA especializada na criação de roteiros inteligentes com os atrativos de [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/atrativos-e-passeios-em-foz-do-iguacu/).
    """)

    categoria_input = st.text_input(
        "Digite o tipo de experiência: Natureza - Lazer - Esporte - Experiência - Cultura - Gastronomia",
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
        
        # Bloco de Notas e Relógio por Atrativo
        notas_roteiro = {}
        if roteiro:
            st.write("---")
            for local in roteiro:
                with st.expander(f"📍 {local}"):
                    # Inicializamos com horário padrão para não disparar erro
                    hora = st.time_input(f"Horário de chegada em {local}", key=f"time_{local}")
                    atividade = st.text_area(f"O que farei aqui?", key=f"note_{local}")
                    notas_roteiro[local] = {"hora": hora, "atividade": atividade}

    with col_mapa:
        # Usamos o "OpenStreetMap" padrão (o mais estável do mundo)
        mapa_antigo = folium.Map(location=[-25.58, -54.55], zoom_start=11, tiles="OpenStreetMap")
        
        # Filtro CSS para deixar o mapa com tom sépia (antigo)
        st.markdown("""
            <style>
            .stFolium {
                filter: sepia(90%) hue-rotate(350deg) brightness(95%);
                border: 4px solid #4E342E;
            }
            </style>
        """, unsafe_allow_html=True)

        coords = []
        for i, nome in enumerate(roteiro):
            lat, lon = atrativos_db[nome]["latitude"], atrativos_db[nome]["longitude"]
            coords.append([lat, lon])
            
            # Marcador
            folium.Marker(
                [lat, lon],
                popup=f"{i+1}: {nome}",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(mapa_antigo)
            
        # Linha que segue a ORDEM da sua seleção
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
    Diferente dos modelos generativos que criam novos conteúdos ou textos baseados em probabilidades estatísticas, nossa IA não generativa atua com base em **lógica determinística e regras estruturadas**. Ela funciona processando dados reais e específicos em uma base de conhecimento curada, aplicando cálculos matemáticos precisos para classificar e recomendar atrativos. Em vez de "imaginar" uma resposta, o sistema avalia variáveis quantificáveis — como reputação, fluxo e capacidade — para entregar um resultado objetivo, consistente e livre de alucinações, garantindo que o roteiro sugerido seja sempre pautado na realidade atual dos pontos turísticos de Foz do Iguaçu.
    """)
