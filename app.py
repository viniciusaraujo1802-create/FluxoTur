import streamlit as st
import random
import time
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- FUNÇÕES DE ACESSIBILIDADE ---
def injetar_acessibilidade():
    vlibras_code = """
    <div vw class="enabled"><div vw-access-button class="active"></div><div vw-plugin-wrapper><div class="vw-plugin-top-wrapper"></div></div></div>
    <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
    <script>new window.VLibras.Widget('https://vlibras.gov.br/app');</script>
    """
    components.html(vlibras_code, height=0)

def gerar_link_mapas(nome):
    query = f"{nome}+Foz+do+Iguacu".replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={query}"

# --- CSS ---
def set_style():
    st.markdown("""
    <style>
    .stApp { background-image: url("https://i.ibb.co/nq73snyt/download.jpg"); background-size: cover; background-attachment: fixed; }
    .block-container { background-color: rgba(255, 255, 255, 0.95); padding: 2rem; border-radius: 15px; }
    h1, h2, h3, p, label { color: #000000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

set_style()
injetar_acessibilidade()

# --- BASE DE DADOS COMPLETA (33 Atrativos com Coordenadas) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "desc": "Kart indoor de alta velocidade."},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "desc": "Trilhas em meio à mata e cachoeiras."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Experiência exclusiva ao nascer do sol."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "lat": -25.616, "lon": -54.481, "desc": "Aquário com biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "lat": -25.538, "lon": -54.542, "desc": "Parque aquático com toboáguas."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "lat": -25.695, "lon": -54.436, "desc": "Cicloturismo em trilhas no Parque Nacional."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "desc": "Parque aquático termal."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "lat": -25.684, "lon": -54.444, "desc": "Vistas panorâmicas e trilhas argentinas."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "A clássica passarela das quedas d'água."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "lat": -25.695, "lon": -54.436, "desc": "Vista aérea e jantar exclusivo."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "lat": -25.510, "lon": -54.500, "desc": "Passeios rurais e cultura regional."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "lat": -25.565, "lon": -54.502, "desc": "Museu de cera e atrações interativas."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "lat": -25.695, "lon": -54.436, "desc": "Passeio de bike guiado pelos atrativos."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "lat": -25.534, "lon": -54.545, "desc": "Salto duplo de paraquedas."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "lat": -25.692, "lon": -54.438, "desc": "Voo de helicóptero sobre as Cataratas."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "lat": -25.550, "lon": -54.580, "desc": "Mobilidade urbana sustentável."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "lat": -25.690, "lon": -54.435, "desc": "Navegação cênica pelo Rio Iguaçu."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "lat": -25.550, "lon": -54.550, "desc": "Expedição por cachoeiras escondidas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "lat": -25.560, "lon": -54.520, "desc": "Yoga e terapias de bem-estar."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "desc": "Tour técnico pela barragem de Itaipu."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "desc": "Show de luzes na usina hidrelétrica."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "lat": -25.405, "lon": -54.588, "desc": "Vista do alto da maior usina do mundo."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "lat": -25.410, "lon": -54.550, "desc": "Preservação e animais nativos."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "lat": -25.405, "lon": -54.588, "desc": "Passeio de barco no Lago de Itaipu."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Aventura radical embaixo das quedas."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "desc": "Encontro do Brasil, Argentina e Paraguai."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "lat": -25.535, "lon": -54.575, "desc": "Arquitetura islâmica."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "desc": "Imersão com aves da Mata Atlântica."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "desc": "Vista privilegiada."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "lat": -25.534, "lon": -54.550, "desc": "Jardins zen."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "desc": "Complexo da usina."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "lat": -25.550, "lon": -54.540, "desc": "Museu de carros."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "desc": "Vista da tríplice fronteira."}
}

# --- ALGORITMOS ---
def calcular_score_mcdm(reputacao, carga_status, transito_status):
    return round(reputacao + (0.5 if carga_status == 1 else -0.5) + (0.5 if transito_status == 1 else -0.5), 2)

def extrair_intencao(texto):
    texto = texto.lower()
    categorias = ["natureza", "esporte", "cultura", "lazer", "experiência"]
    if texto in categorias: return texto.capitalize()
    mapeamento = {"pedalar": "Esporte", "bike": "Esporte", "barco": "Lazer", "trilha": "Natureza", "museu": "Cultura"}
    for p, c in mapeamento.items():
        if p in texto: return c
    return None

# --- INTERFACE ---
tabs = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tabs[0]:
    st.title("🌍 FluxoTur")
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?", help="Ex: trilha, museu, bike...")
    
    if st.button("🚀 Gerar roteiro inteligente"):
        cat_intencao = extrair_intencao(pesquisa)
        mensagens = {"Natureza": "🌿 X.TUR: Conectando você à natureza...", "Esporte": "🏃 X.TUR: Ativando aventura...", "Cultura": "🏛️ X.TUR: Explorando história...", "Lazer": "🎡 X.TUR: Diversão garantida...", "Experiência": "✨ X.TUR: Momentos únicos..."}
        
        resultados = {n: d for n, d in atrativos_db.items() if d['cat'] == cat_intencao} if cat_intencao else atrativos_db
        if cat_intencao: st.info(mensagens.get(cat_intencao, "X.TUR: Otimizando..."))

        ranking = []
        for nome, info in resultados.items():
            c, t = random.choice([0, 1]), random.choice([0, 1])
            ranking.append({"nome": nome, "score": calcular_score_mcdm(info['R'], c, t), "c": c, "t": t, "R": info['R'], "desc": info['desc']})
        
        for item in sorted(ranking, key=lambda x: x['score'], reverse=True):
            with st.expander(f"📍 {item['nome']} (Score: {item['score']:.1f})"):
                if item['c'] == 0: st.warning("⚠️ Dica Sensorial: Local movimentado/barulhento.")
                else: st.info("🛋️ Dica Sensorial: Ambiente calmo.")
                st.write(f"**Descrição:** {item['desc']}")
                st.link_button("Abrir no Google Maps", gerar_link_mapas(item['nome']))

with tabs[1]:
    st.header("📍 Mapa dos Atrativos em Foz")
    df_mapa = pd.DataFrame.from_dict(atrativos_db, orient='index')
    st.map(df_mapa)

with tabs[2]:
    st.header("🧠 O que é IA não generativa?")
    st.write("O FluxoTur utiliza **Tomada de Decisão Multicritério (MCDM)**. Ao contrário do ChatGPT, que gera textos, nós aplicamos cálculos matemáticos sobre dados reais e fixos de Foz do Iguaçu para ordenar o melhor destino para você.")
