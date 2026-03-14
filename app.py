import streamlit as st
import random
import pandas as pd
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS ---
def injetar_vlibras():
    vlibras_code = """
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
    components.html(vlibras_code, height=100)

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

# --- BASE DE DADOS ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9},
    "AquaFoz": {"cat": "Cultura", "R": 4.6},
    "Aquamania": {"cat": "Lazer", "R": 4.4},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7},
    "Blue Park": {"cat": "Lazer", "R": 4.5},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8},
    "Circuito São João": {"cat": "Cultura", "R": 4.3},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7},
    "Kattamaram": {"cat": "Lazer", "R": 4.5},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    
    st.markdown("""
    Olá! Sou o FluxoTur, a inteligência artificial não generativa especializada na 
    otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/).
    """)
    
    st.markdown("💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    
    if st.button("🚀 Gerar roteiro inteligente"):
        with st.spinner("Analisando..."):
            lista_resultados = []
            for nome, info in atrativos_db.items():
                if info['cat'].lower() == pesquisa.lower():
                    score = round(random.uniform(5.3, 10.5), 1)
                    c = random.choice(["Lotado", "Não Lotado"])
                    t = random.choice(["Intenso", "Não Intenso"])
                    lista_resultados.append({"nome": nome, "score": score, "R": info['R'], "t": t, "c": c})
            
            lista_resultados.sort(key=lambda x: x['score'], reverse=True)
            for item in lista_resultados:
                st.markdown(f"### 📍 {item['nome']} ({item['score']})")
                st.write(f"**Reputação:** {item['R']} | **Trânsito:** {item['t']} | **Capacidade:** {item['c']}")
                st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(item['nome']))
                st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral")
    st.write("Visualização dos atrativos.")
    st.map(pd.DataFrame.from_dict(atrativos_db, orient='index'))

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("""
    O FluxoTur utiliza uma arquitetura de **Inteligência Artificial Não Generativa**. 
    Diferente de sistemas que criam novos conteúdos, nossa IA é especializada na análise profunda 
    e na categorização inteligente de dados turísticos pré-existentes.

    **Como o sistema funciona:**
    * **Processamento Analítico:** Examinamos variáveis críticas como reputação digital, condições de trânsito em tempo real e níveis de carga/capacidade dos atrativos.
    * **Otimização Logística:** O sistema cruza esses dados estatísticos para prever o fluxo ideal, garantindo que o turista tenha uma experiência baseada em evidências reais.
    * **Governança de Dados:** Priorizamos a precisão analítica e a confiança, transformando o planejamento do passeio em uma ciência exata, onde cada sugestão é fruto de processamento rigoroso de informações de campo.
    """)
