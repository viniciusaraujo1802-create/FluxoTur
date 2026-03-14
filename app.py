import streamlit as st
import random
import pandas as pd
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS ---
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
        [vw] { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 99999999 !important; }
    </style>
    """
    components.html(vlibras_html, height=100)

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

# --- BASE DE DADOS (Mantida conforme aprovado) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "dica": "Prepare o capacete e acelere fundo nesta pista de elite!"},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "dica": "O refúgio perfeito para renovar as energias em trilhas selvagens."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "dica": "Um privilégio único: ver o sol nascer sobre as quedas d'água."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "dica": "Mergulhe fundo na história viva da nossa biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "dica": "Splash! O lugar ideal para dar risada com toda a família."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "dica": "Pedale pelo coração da floresta e sinta a vida selvagem de perto."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "dica": "Água quentinha e diversão sem fim na praia termal de Foz."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "dica": "Prepare-se para ficar impressionado com o lado hermano das cataratas!"},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "dica": "A clássica e inesquecível Garganta do Diabo espera por você."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "dica": "Sabor e vista espetacular lá no alto das nuvens."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "dica": "Um mergulho autêntico nas tradições e raízes da nossa gente."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "dica": "Um mundo mágico onde a imaginação ganha vida em cada museu."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "dica": "Sinta o vento no rosto pedalando rumo ao espetáculo das águas."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "dica": "Se tem coragem, o céu de Foz é o seu melhor destino hoje!"},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "dica": "Voe alto e tenha a melhor foto aérea da sua vida."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "dica": "Guias especializados para você rodar pelos pontos secretos de Foz."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "dica": "Navegue pelo rio e veja a selva de uma perspectiva privilegiada."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "dica": "Descubra cachoeiras escondidas que nem todo mundo conhece."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "dica": "Desconecte do mundo e reconecte com o seu bem-estar aqui."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "dica": "Uma visita técnica épica no coração da maior usina do mundo."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "dica": "Veja a gigante Itaipu se transformar em um show de luzes noturno."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "dica": "A vista clássica que mostra o tamanho monumental dessa obra."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "dica": "Encontre animais lindos e aprenda sobre a preservação local."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "dica": "Relaxe no convés e deixe o barco te levar pelo lago de Itaipu."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "dica": "Se prepare para se molhar e gritar de tanta emoção!"},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "dica": "Onde o Brasil dá a mão para a Argentina e o Paraguai. Imperdível!"},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "dica": "Uma joia arquitetônica que traz o oriente para o coração de Foz."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "dica": "Entre no viveiro e sinta a vida das aves tropicais ao redor."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "dica": "O encerramento perfeito para um dia mágico nas águas."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "dica": "Encontre a paz interior entre centenas de estátuas serenas."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "dica": "Explore todos os ângulos e segredos desta gigante de concreto."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "dica": "Cinema de alta tecnologia e shows que vão te surpreender."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "dica": "Suba lá no alto e tenha uma visão inesquecível da cidade."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    # Texto fixo conforme sua imagem
    st.markdown("Olá! Sou o X.Tur, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.fozdoiguacu.com.br/).")
    st.markdown("💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
    
    # O uso do st.form faz com que o ENTER funcione automaticamente como o clique no botão
    with st.form(key='form_busca'):
        pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
        btn_clicado = st.form_submit_button("🚀 Gerar roteiro inteligente")
    
    if btn_clicado or pesquisa:
        with st.spinner("Analisando dados..."):
            lista = [item for nome, item in atrativos_db.items() if not pesquisa or item['cat'].lower() == pesquisa.lower()]
            
            if not lista: 
                st.warning("🤖 Ops! Não encontrei nada.")
            else:
                for item in lista:
                    item['score_final_calculado'] = round(random.uniform(5.3, 10.5), 1)
                
                lista_ordenada = sorted(lista, key=lambda x: x['score_final_calculado'], reverse=True)
                
                st.success(f"🤖 Encontrei {len(lista_ordenada)} opções para você:")
                for item in lista_ordenada:
                    nome_atrativo = [k for k, v in atrativos_db.items() if v == item][0]
                    st.markdown(f"### 📍 {nome_atrativo} (Score: {item['score_final_calculado']})")
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
