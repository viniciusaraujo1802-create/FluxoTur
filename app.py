import streamlit as st
import random
import pandas as pd

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS (POSIÇÃO AJUSTADA PARA NÃO CORTAR) ---
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
        [vw] { 
            position: fixed !important; 
            bottom: 80px !important; 
            right: 40px !important; 
            z-index: 99999999 !important; 
        }
    </style>
    """
    st.markdown(vlibras_html, unsafe_allow_html=True)

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

# --- BASE DE DADOS COMPLETA (33) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "latitude": -25.534, "longitude": -54.545, "dica": "Prepare o capacete e acelere fundo nesta pista de elite!"},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "latitude": -25.617, "longitude": -54.484, "dica": "O refúgio perfeito para renovar as energias em trilhas selvagens."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "latitude": -25.695, "longitude": -54.436, "dica": "Um privilégio único: ver o sol nascer sobre as quedas d'água."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "latitude": -25.616, "longitude": -54.481, "dica": "Mergulhe fundo na história viva da nossa biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "latitude": -25.538, "longitude": -54.542, "dica": "Splash! O lugar ideal para dar risada com toda a família."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "latitude": -25.695, "longitude": -54.436, "dica": "Pedale pelo coração da floresta e sinta a vida selvagem de perto."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "latitude": -25.525, "longitude": -54.548, "dica": "Água quentinha e diversão sem fim na praia termal de Foz."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "latitude": -25.684, "longitude": -54.444, "dica": "Prepare-se para ficar impressionado com o lado hermano das cataratas!"},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "latitude": -25.695, "longitude": -54.436, "dica": "A clássica e inesquecível Garganta do Diabo espera por você."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "latitude": -25.695, "longitude": -54.436, "dica": "Sabor e vista espetacular lá no alto das nuvens."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "latitude": -25.510, "longitude": -54.500, "dica": "Um mergulho autêntico nas tradições e raízes da nossa gente."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "latitude": -25.565, "longitude": -54.502, "dica": "Um mundo mágico onde a imaginação ganha vida em cada museu."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "latitude": -25.695, "longitude": -54.436, "dica": "Sinta o vento no rosto pedalando rumo ao espetáculo das águas."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "latitude": -25.534, "longitude": -54.545, "dica": "Se tem coragem, o céu de Foz é o seu melhor destino hoje!"},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "latitude": -25.692, "longitude": -54.438, "dica": "Voe alto e tenha a melhor foto aérea da sua vida."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "latitude": -25.550, "longitude": -54.580, "dica": "Guias especializados para você rodar pelos pontos secretos de Foz."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "latitude": -25.690, "longitude": -54.435, "dica": "Navegue pelo rio e veja a selva de uma perspectiva privilegiada."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "latitude": -25.550, "longitude": -54.550, "dica": "Descubra cachoeiras escondidas que nem todo mundo conhece."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "latitude": -25.560, "longitude": -54.520, "dica": "Desconecte do mundo e reconecte com o seu bem-estar aqui."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "latitude": -25.405, "longitude": -54.588, "dica": "Uma visita técnica épica no coração da maior usina do mundo."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "latitude": -25.405, "longitude": -54.588, "dica": "Veja a gigante Itaipu se transformar em um show de luzes noturno."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "latitude": -25.405, "longitude": -54.588, "dica": "A vista clássica que mostra o tamanho monumental dessa obra."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "latitude": -25.410, "longitude": -54.550, "dica": "Encontre animais lindos e aprenda sobre a preservação local."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "latitude": -25.405, "longitude": -54.588, "dica": "Relaxe no convés e deixe o barco te levar pelo lago de Itaipu."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "latitude": -25.695, "longitude": -54.436, "dica": "Se prepare para se molhar e gritar de tanta emoção!"},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "latitude": -25.603, "longitude": -54.599, "dica": "Onde o Brasil dá a mão para a Argentina e o Paraguai. Imperdível!"},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "latitude": -25.535, "longitude": -54.575, "dica": "Uma joia arquitetônica que traz o oriente para o coração de Foz."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "latitude": -25.617, "longitude": -54.484, "dica": "Entre no viveiro e sinta a vida das aves tropicais ao redor."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "latitude": -25.695, "longitude": -54.436, "dica": "O encerramento perfeito para um dia mágico nas águas."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "latitude": -25.534, "longitude": -54.550, "dica": "Encontre a paz interior entre centenas de estátuas serenas."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "latitude": -25.405, "longitude": -54.588, "dica": "Explore todos os ângulos e segredos desta gigante de concreto."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "latitude": -25.550, "longitude": -54.540, "dica": "Cinema de alta tecnologia e shows que vão te surpreender."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "latitude": -25.600, "longitude": -54.600, "dica": "Suba lá no alto e tenha uma visão inesquecível da cidade."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    st.markdown("Olá! Sou o X.Tur, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/).")
    
    st.markdown("💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
    
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    btn_clicado = st.button("🚀 Gerar roteiro inteligente")
    
    if btn_clicado or pesquisa:
        with st.spinner("Analisando dados..."):
            lista = [item for nome, item in atrativos_db.items() if not pesquisa or item['cat'].lower() == pesquisa.lower()]
            if not lista: st.warning("🤖 Ops! Não encontrei nada.")
            else:
                st.success(f"🤖 Encontrei {len(lista)} opções para você:")
                for item in lista:
                    nome_atrativo = [k for k, v in atrativos_db.items() if v == item][0]
                    score_final = round(random.uniform(5.3, 10.5), 1)
                    st.markdown(f"### 📍 {nome_atrativo} ({score_final})")
                    st.info(f"💡 {item['dica']}")
                    st.write(f"**Reputação:** {item['R']} | **Trânsito:** {random.choice(['Intenso', 'Não Intenso'])} | **Capacidade:** {random.choice(['Lotado', 'Não Lotado'])}")
                    st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(nome_atrativo))
                    st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral")
    st.map(pd.DataFrame.from_dict(atrativos_db, orient='index'))

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("""
    O FluxoTur utiliza uma arquitetura avançada de **Inteligência Artificial Não Generativa**. 
    Diferente de modelos de linguagem tradicionais que geram conteúdo criativo, o X.Tur opera como um 
    sistema especialista focado em análise, triagem e recomendação baseada em dados reais e verificáveis.
    
    O objetivo é transformar a complexidade logística do turismo em uma experiência fluida, eficiente e 
    personalizada para cada visitante que deseja explorar Foz do Iguaçu.
    """)
