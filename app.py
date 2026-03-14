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
    /* Forçar texto em preto e negrito */
    .stApp, .stMarkdown, .stText, .stTextInput, .stButton, p, h1, h2, h3, div, label, span {{
        color: #000000 !important;
        font-weight: bold !important;
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
      window.onload = function() {
        new window.VLibras.Widget('https://vlibras.gov.br/app');
      }
    </script>
    """
    st.components.v1.html(vlibras_html, height=0)

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
    "Blue Park":{"cat":"Lazer","latitude":-25.525,"longitude":-54.548,"dica":"Praia termal artificial com águas aquecidas."},
    "Cataratas del Iguazú – Argentina":{"cat":"Natureza","latitude":-25.684,"longitude":-54.444,"dica":"O lado argentino das cataratas com trilhas panorâmicas."},
    "Cataratas do Iguaçu – Brasil":{"cat":"Natureza","latitude":-25.695,"longitude":-54.436,"dica":"A famosa Garganta do Diabo vista do lado brasileiro."},
    "Dreams Park Show":{"cat":"Lazer","latitude":-25.565,"longitude":-54.502,"dica":"Complexo com museus e atrações temáticas."},
    "Itaipu Especial":{"cat":"Cultura","latitude":-25.405,"longitude":-54.588,"dica":"Visita técnica ao interior da usina."},
    "Marco das Três Fronteiras":{"cat":"Cultura","latitude":-25.603,"longitude":-54.599,"dica":"Ponto onde se encontram Brasil, Argentina e Paraguai."},
    "Parque das Aves":{"cat":"Natureza","latitude":-25.617,"longitude":-54.484,"dica":"Parque dedicado à conservação de aves tropicais."},
    "Rafain Churrascaria":{"cat":"Gastronomia","latitude":-25.547,"longitude":-54.585,"dica":"Churrascaria tradicional com show latino-americano."},
    "Yup Star – Roda Gigante":{"cat":"Lazer","latitude":-25.600,"longitude":-54.600,"dica":"Roda gigante com vista panorâmica de Foz."}
}

# ---------------- INTERFACE ----------------
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    categoria_input = st.text_input("Digite o tipo de experiência: Natureza - Lazer - Esporte - Experiência - Cultura - Gastronomia")
    btn = st.button("🚀 Gerar roteiro inteligente")

    if btn:
        resultados = []
        for nome, item in atrativos_db.items():
            if not categoria_input or categoria_input.strip().lower() in item["cat"].lower():
                # Metodologia de Cálculo
                reputacao = round(random.uniform(3.0, 4.9), 1)
                transito = random.choice(["Intenso", "Não Intenso"])
                capacidade = random.choice(["Lotado", "Não Lotado"])
                
                transito_peso = 1.0 if transito == "Não Intenso" else 0.5
                capacidade_peso = 1.0 if capacidade == "Não Lotado" else 0.5
                
                # O Score agora segue uma lógica real baseada nos pesos
                score = round((reputacao * 2) + transito_peso + capacidade_peso, 1)

                resultados.append({
                    "nome": nome, "score": score, "reputacao": reputacao,
                    "transito": transito, "capacidade": capacidade, "item": item
                })

        resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)
        st.success(f"Aqui estão os {len(resultados)} locais encontrados")

        for r in resultados:
            st.markdown(f"### 📍 {r['nome']} ⭐ {r['score']}")
            st.write(f"**Reputação:** {r['reputacao']} | **Trânsito:** {r['transito']} | **Capacidade:** {r['capacidade']}")
            st.info(f"💡 {r['item']['dica']}")
            st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(r["nome"]))
            st.markdown("---")

with tab2:
    mapa = folium.Map(location=[-25.58, -54.55], zoom_start=10)
    for nome, item in atrativos_db.items():
        folium.Marker([item["latitude"], item["longitude"]], popup=nome).add_to(mapa)
    st_folium(mapa, use_container_width=True, height=600)

with tab3:
    st.header("🧠 Entenda o FluxoTur")
    st.write("O FluxoTur utiliza uma metodologia de cálculo ponderado onde o score final é definido por: **(Reputação × 2) + Peso do Trânsito + Peso da Capacidade**.")
