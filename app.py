import streamlit as st
import random
import time
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO E VLIBRAS ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

def injetar_vlibras():
    vlibras_code = """
    <div vw class="enabled"><div vw-access-button class="active"></div><div vw-plugin-wrapper><div class="vw-plugin-top-wrapper"></div></div></div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>new window.VLibras.Widget('https://vlibras.gov.br/app');</script>
    """
    components.html(vlibras_code, height=0)

injetar_vlibras()

# --- FUNÇÃO DE LINKS ---
def gerar_link_mapas(nome):
    query = f"{nome}+Foz+do+Iguacu".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={query}"

# --- ESTILO ---
st.markdown("""
<style>
.stApp { background-image: url("https://i.ibb.co/nq73snyt/download.jpg"); background-size: cover; background-position: center; background-attachment: fixed; }
.block-container { background-color: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; }
h1, h2, h3, p, label { color: #000000 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- DADOS (Escala 2.5 a 5.0) ---
atrativos_db = {
    "Cataratas do Iguaçu": {"cat": "Natureza", "R": 5.0, "desc": "Quedas d'água mundialmente famosas."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "desc": "Imersão na fauna local."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "desc": "Encontro entre Brasil, Argentina e Paraguai."},
    "Usina de Itaipu": {"cat": "Cultura", "R": 4.7, "desc": "Maior usina hidrelétrica em produção."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "desc": "Passeio de barco radical."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "desc": "Parque aquático termal."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.4, "desc": "Museu de cera e atrações."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.6, "desc": "Yoga e terapias de relaxamento."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "desc": "Jantar exclusivo com vista."},
    "Kartódromo Adrena Kart": {"cat": "Esporte", "R": 4.2, "desc": "Pista de kart profissional."}
    # [Adicione o restante aqui seguindo este padrão, garantindo R entre 2.5 e 5.0]
}

# --- ABAS E INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro - Foz do Iguaçu")
    pesquisa = st.selectbox("💬 Escolha o tipo de turismo:", ["Natureza", "Esporte", "Cultura", "Lazer", "Experiência"])
    
    if st.button("🚀 Gerar roteiro inteligente"):
        st.info(f"X.TUR: Analisando {pesquisa}...")
        with st.spinner("Processando dados de trânsito e carga..."):
            time.sleep(1)
            for nome, info in atrativos_db.items():
                if info['cat'] == pesquisa:
                    c = random.choice(["Lotado", "Não Lotado"])
                    t = random.choice(["Intenso", "Não Intenso"])
                    st.markdown(f"### 📍 {nome}")
                    st.write(f"**Reputação:** {info['R']} | **Trânsito:** {t} | **Carga:** {c}")
                    st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(nome))
                    st.markdown("---")

with tab2:
    st.write("Mapa em construção...")

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("Olá, eu sou o **X.Tur**!")
    st.write("""
    A inteligência artificial não generativa diferencia-se por focar no exame e na categorização de dados pré-existentes para a formulação de previsões. 
    Esta distinção é fundamental para sistemas que priorizam a precisão analítica sobre a criação de conteúdo, 
    permitindo uma governança baseada em evidências estatísticas.
    """)import streamlit as st
import random
import time
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO E VLIBRAS ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

def injetar_vlibras():
    vlibras_code = """
    <div vw class="enabled"><div vw-access-button class="active"></div><div vw-plugin-wrapper><div class="vw-plugin-top-wrapper"></div></div></div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>new window.VLibras.Widget('https://vlibras.gov.br/app');</script>
    """
    components.html(vlibras_code, height=0)

injetar_vlibras()

# --- FUNÇÃO DE LINKS ---
def gerar_link_mapas(nome):
    query = f"{nome}+Foz+do+Iguacu".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={query}"

# --- ESTILO ---
st.markdown("""
<style>
.stApp { background-image: url("https://i.ibb.co/nq73snyt/download.jpg"); background-size: cover; background-position: center; background-attachment: fixed; }
.block-container { background-color: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; }
h1, h2, h3, p, label { color: #000000 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- DADOS (Escala 2.5 a 5.0) ---
atrativos_db = {
    "Cataratas do Iguaçu": {"cat": "Natureza", "R": 5.0, "desc": "Quedas d'água mundialmente famosas."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "desc": "Imersão na fauna local."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "desc": "Encontro entre Brasil, Argentina e Paraguai."},
    "Usina de Itaipu": {"cat": "Cultura", "R": 4.7, "desc": "Maior usina hidrelétrica em produção."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "desc": "Passeio de barco radical."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "desc": "Parque aquático termal."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.4, "desc": "Museu de cera e atrações."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.6, "desc": "Yoga e terapias de relaxamento."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "desc": "Jantar exclusivo com vista."},
    "Kartódromo Adrena Kart": {"cat": "Esporte", "R": 4.2, "desc": "Pista de kart profissional."}
    # [Adicione o restante aqui seguindo este padrão, garantindo R entre 2.5 e 5.0]
}

# --- ABAS E INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro - Foz do Iguaçu")
    pesquisa = st.selectbox("💬 Escolha o tipo de turismo:", ["Natureza", "Esporte", "Cultura", "Lazer", "Experiência"])
    
    if st.button("🚀 Gerar roteiro inteligente"):
        st.info(f"X.TUR: Analisando {pesquisa}...")
        with st.spinner("Processando dados de trânsito e carga..."):
            time.sleep(1)
            for nome, info in atrativos_db.items():
                if info['cat'] == pesquisa:
                    c = random.choice(["Lotado", "Não Lotado"])
                    t = random.choice(["Intenso", "Não Intenso"])
                    st.markdown(f"### 📍 {nome}")
                    st.write(f"**Reputação:** {info['R']} | **Trânsito:** {t} | **Carga:** {c}")
                    st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(nome))
                    st.markdown("---")

with tab2:
    st.write("Mapa em construção...")

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("Olá, eu sou o **X.Tur**!")
    st.write("""
    A inteligência artificial não generativa diferencia-se por focar no exame e na categorização de dados pré-existentes para a formulação de previsões. 
    Esta distinção é fundamental para sistemas que priorizam a precisão analítica sobre a criação de conteúdo, 
    permitindo uma governança baseada em evidências estatísticas.
    """)
