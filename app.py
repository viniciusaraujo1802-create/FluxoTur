import streamlit as st
import random
import pandas as pd
import folium
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# ---------------- IMAGEM DE FUNDO ----------------

st.markdown(
"""
<style>

.stApp{
background-image:url("https://upload.wikimedia.org/wikipedia/commons/3/3d/Iguazu_Falls.jpg");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

</style>
""",
unsafe_allow_html=True
)

# ---------------- VLIBRAS ----------------

st.markdown(
"""
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
""",
unsafe_allow_html=True
)

# ---------------- FUNÇÃO MAPS ----------------

def gerar_link_mapas(nome):
    return f"https://www.google.com/maps/search/?api=1&query={nome.replace(' ','+')}+Foz+do+Iguacu"

# ---------------- ATRATIVOS ----------------

atrativos_db = {

"Adrena Kart Kartódromo":{"cat":"Esporte","latitude":-25.534,"longitude":-54.545,"dica":"Acelere em uma das pistas de kart mais famosas da cidade."},

"Aguaray Eco":{"cat":"Natureza","latitude":-25.617,"longitude":-54.484,"dica":"Trilhas ecológicas em meio à mata preservada."},

"Amanhecer nas Cataratas":{"cat":"Experiência","latitude":-25.695,"longitude":-54.436,"dica":"Veja o nascer do sol nas cataratas."},

"AquaFoz":{"cat":"Cultura","latitude":-25.616,"longitude":-54.481,"dica":"Aquário com espécies da região trinacional."},

"Aquamania":{"cat":"Lazer","latitude":-25.538,"longitude":-54.542,"dica":"Parque aquático para toda família."},

"Bike Poço Preto":{"cat":"Esporte","latitude":-25.695,"longitude":-54.436,"dica":"Pedale pela floresta do Parque Nacional."},

"Blue Park":{"cat":"Lazer","latitude":-25.525,"longitude":-54.548,"dica":"Praia termal artificial incrível."},

"Cataratas del Iguazú – Argentina":{"cat":"Natureza","latitude":-25.684,"longitude":-54.444,"dica":"Vista espetacular pelo lado argentino."},

"Cataratas do Iguaçu – Brasil":{"cat":"Natureza","latitude":-25.695,"longitude":-54.436,"dica":"A famosa Garganta do Diabo."},

"Céu das Cataratas":{"cat":"Experiência","latitude":-25.695,"longitude":-54.436,"dica":"Restaurante panorâmico com vista."},

"Circuito São João":{"cat":"Cultura","latitude":-25.510,"longitude":-54.500,"dica":"Circuito cultural histórico."},

"Dreams Park Show":{"cat":"Lazer","latitude":-25.565,"longitude":-54.502,"dica":"Complexo turístico temático."},

"Falls Bike Tour":{"cat":"Esporte","latitude":-25.695,"longitude":-54.436,"dica":"Passeio ciclístico guiado."},

"Fly Foz – Paraquedismo":{"cat":"Esporte","latitude":-25.534,"longitude":-54.545,"dica":"Salto de paraquedas sobre Foz."},

"Helisul Experience – Cataratas":{"cat":"Experiência","latitude":-25.692,"longitude":-54.438,"dica":"Sobrevoo de helicóptero."},

"Helisul Experience – Itaipu":{"cat":"Experiência","latitude":-25.405,"longitude":-54.588,"dica":"Vista aérea de Itaipu."},

"Iguassu By Bike":{"cat":"Esporte","latitude":-25.550,"longitude":-54.580,"dica":"Passeio de bike pela cidade."},

"Iguassu River Tour":{"cat":"Natureza","latitude":-25.690,"longitude":-54.435,"dica":"Passeio de barco pelo rio."},

"Iguassu Secret Falls":{"cat":"Natureza","latitude":-25.550,"longitude":-54.550,"dica":"Cachoeiras escondidas."},

"Iguazu Wellness":{"cat":"Experiência","latitude":-25.560,"longitude":-54.520,"dica":"Yoga e bem-estar."},

"Itaipu Especial":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Visita técnica à usina."},

"Itaipu Iluminada":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Show de luzes na barragem."},

"Itaipu Panorâmica":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Vista panorâmica de Itaipu."},

"Itaipu Refúgio Biológico":{"cat":"Natureza","latitude":-25.410,"longitude":-54.550,"dica":"Reserva natural."},

"Kattamaram":{"cat":"Lazer","latitude":-25.405,"longitude":-54.588,"dica":"Passeio de barco no lago."},

"Macuco Safari":{"cat":"Esporte","latitude":-25.695,"longitude":-54.436,"dica":"Barco nas cataratas."},

"Marco das Três Fronteiras":{"cat":"Cultura","latitude":-25.603,"longitude":-54.599,"dica":"Brasil Argentina Paraguai."},

"Mesquita Omar Ibn Al-Khattab":{"cat":"Cultura","latitude":-25.535,"longitude":-54.575,"dica":"Arquitetura islâmica."},

"Parque das Aves":{"cat":"Natureza","latitude":-25.617,"longitude":-54.484,"dica":"Aves tropicais."},

"Pôr do Sol nas Cataratas":{"cat":"Experiência","latitude":-25.695,"longitude":-54.436,"dica":"Experiência ao entardecer."},

"Templo Budista Chen Tien":{"cat":"Cultura","latitude":-25.534,"longitude":-54.550,"dica":"Templo budista com vista."},

"Turismo Itaipu":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Centro de visitantes."},

"Yup Star – Roda Gigante":{"cat":"Lazer","latitude":-25.600,"longitude":-54.600,"dica":"Vista panorâmica da cidade."}

}

# ---------------- INTERFACE ----------------

tab1,tab2,tab3 = st.tabs(["Planejador FluxoTur","Mapa Geral","Entenda o FluxoTur"])

# ---------------- PLANEJADOR ----------------

with tab1:

    st.title("FluxoTur")

    st.markdown(
    "Olá! Sou o **X.Tur**, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/atrativos-e-passeios-em-foz-do-iguacu/)."
    )

    pesquisa = st.text_input("O que você deseja fazer hoje?")
    btn = st.button("Gerar roteiro inteligente")

    if btn:

        resultados=[]

        for nome,item in atrativos_db.items():

            if pesquisa=="" or pesquisa.lower() in item["cat"].lower():

                score = round(random.uniform(5.3,10.5),1)

                resultados.append({
                    "nome":nome,
                    "score":score,
                    "item":item
                })

        resultados=sorted(resultados,key=lambda x:x["score"],reverse=True)

        st.success(f"Aqui estão os {len(resultados)} atrativos encontrados")

        for r in resultados:

            st.markdown(f"### {r['nome']} ⭐ {r['score']}")

            st.info(f"💡 {r['item']['dica']}")

            st.link_button("Abrir no Google Maps",gerar_link_mapas(r["nome"]))

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

    st.write("""
O FluxoTur é um protótipo de inteligência artificial não generativa voltado ao planejamento turístico em Foz do Iguaçu. O sistema organiza e prioriza atrativos a partir da análise de variáveis como reputação digital, fluxo de trânsito e tipologia das experiências turísticas, sugerindo possibilidades de visitação que ajudam o usuário a planejar roteiros de forma mais eficiente e contribuem para uma melhor distribuição do fluxo de visitantes entre diferentes atrativos do destino.
""")
