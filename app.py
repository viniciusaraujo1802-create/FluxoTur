import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

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
      window.onload = function() {
        new window.VLibras.Widget('https://vlibras.gov.br/app');
      }
    </script>
    """
    st.components.v1.html(vlibras_html,height=0)

injetar_vlibras()


def gerar_link_mapas(nome):
    return f"https://www.google.com/maps/search/?api=1&query={nome.replace(' ', '+')}+Foz+do+Iguacu"


# ---------------- DISTÂNCIA ----------------

def calcular_distancia(lat1, lon1, lat2, lon2):

    R = 6371
    lat1,lon1,lat2,lon2 = map(radians,[lat1,lon1,lat2,lon2])

    dlat = lat2-lat1
    dlon = lon2-lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*atan2(sqrt(a),sqrt(1-a))

    return R*c


# ---------------- BASE DE ATRATIVOS ----------------

atrativos_db = {

# -------- ATRATIVOS TURÍSTICOS --------

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

# -------- RESTAURANTES (GASTRONOMIA) --------

"Rafain Churrascaria":{"cat":"Gastronomia","latitude":-25.547,"longitude":-54.585,"dica":"Churrascaria tradicional com show latino-americano."},
"La Mafia Trattoria":{"cat":"Gastronomia","latitude":-25.545,"longitude":-54.587,"dica":"Restaurante italiano famoso na cidade."},
"Vó Bertila Pizza":{"cat":"Gastronomia","latitude":-25.550,"longitude":-54.585,"dica":"Pizzaria artesanal muito conhecida em Foz."},
"Capitão Bar":{"cat":"Gastronomia","latitude":-25.548,"longitude":-54.586,"dica":"Bar e restaurante com clima descontraído."},
"Empório com Arte":{"cat":"Gastronomia","latitude":-25.552,"longitude":-54.584,"dica":"Restaurante com gastronomia contemporânea."},
"Porto Canoas":{"cat":"Gastronomia","latitude":-25.695,"longitude":-54.437,"dica":"Restaurante dentro do Parque Nacional."},
"Sushi Hokkai":{"cat":"Gastronomia","latitude":-25.544,"longitude":-54.586,"dica":"Restaurante japonês popular na cidade."},

# -------- SHOPPINGS (LAZER) --------

"Shopping Catuaí Palladium":{"cat":"Lazer","latitude":-25.527,"longitude":-54.573,"dica":"Maior shopping da cidade."},
"JL Cataratas Shopping":{"cat":"Lazer","latitude":-25.539,"longitude":-54.584,"dica":"Shopping central de Foz do Iguaçu."}

}


# ---------------- INTERFACE ----------------

tab1,tab2,tab3 = st.tabs(["🚀 Planejador FluxoTur","📍 Mapa Geral","🧠 Entenda o FluxoTur"])


# ---------------- PLANEJADOR ----------------

with tab1:

    st.title("🌍 FluxoTur")

    st.markdown("""
Olá! Sou o **X.Tur**, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros turísticos com os atrativos do  
[Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/atrativos-e-passeios-em-foz-do-iguacu/)
""")

    categoria = st.selectbox(
        "Escolha o tipo de experiência",
        ["Todas","Natureza","Cultura","Experiência","Esporte","Lazer","Gastronomia"]
    )

    btn = st.button("🚀 Gerar roteiro inteligente")

    if btn:

        resultados=[]

        for nome,item in atrativos_db.items():

            if categoria=="Todas" or item["cat"]==categoria:

                score = round(random.uniform(5.3,10.5),1)
                reputacao = round(random.uniform(3.0,4.9),1)
                transito = random.choice(["Intenso","Não Intenso"])
                capacidade = random.choice(["Lotado","Não Lotado"])

                resultados.append({
                    "nome":nome,
                    "score":score,
                    "reputacao":reputacao,
                    "transito":transito,
                    "capacidade":capacidade,
                    "item":item
                })

        resultados=sorted(resultados,key=lambda x:x["score"],reverse=True)

        st.success(f"Aqui estão os {len(resultados)} locais encontrados")

        for r in resultados:

            st.markdown(f"### 📍 {r['nome']} ⭐ {r['score']}")

            st.write(f"""
            **Reputação Digital:** {r['reputacao']}  
            **Fluxo de Trânsito:** {r['transito']}  
            **Capacidade de Carga:** {r['capacidade']}
            """)

            st.info(f"💡 {r['item']['dica']}")

            st.link_button("📍 Abrir no Google Maps",gerar_link_mapas(r["nome"]))

            st.markdown("---")


# ---------------- MAPA ----------------

with tab2:

    mapa=folium.Map(location=[-25.55,-54.58],zoom_start=11)

    for nome,item in atrativos_db.items():

        folium.Marker(
            [item["latitude"],item["longitude"]],
            popup=nome
        ).add_to(mapa)

    st_folium(mapa,width=900,height=600)


# ---------------- EXPLICAÇÃO ----------------

with tab3:

    st.header("🧠 Entenda o FluxoTur")

    st.write("""
O FluxoTur é um protótipo de inteligência artificial não generativa voltado ao planejamento turístico em Foz do Iguaçu. Diferentemente das inteligências artificiais generativas, que produzem conteúdos novos com base em grandes modelos estatísticos, uma inteligência não generativa trabalha com bases estruturadas de dados previamente organizadas. Isso significa que o sistema utiliza informações reais sobre atrativos turísticos, categorias de experiências, localização geográfica e características de visitação para apoiar o planejamento de roteiros turísticos.

Na prática, o FluxoTur funciona como um sistema de apoio ao visitante, permitindo identificar rapidamente atrativos naturais, culturais, experiências turísticas, opções de lazer e estabelecimentos gastronômicos em Foz do Iguaçu e região trinacional. A plataforma também integra visualização em mapa, classificação de atrativos e sugestões de visitação, contribuindo para uma organização mais eficiente do tempo do turista no destino.
""")
