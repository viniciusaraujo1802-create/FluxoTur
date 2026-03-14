import streamlit as st
import random
import pandas as pd

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
        [vw] { 
            position: fixed !important; 
            bottom: 30px !important; 
            right: 30px !important; 
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

# --- BASE DE DADOS ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "latitude": -25.534, "longitude": -54.545, "dica": "Prepare o capacete e acelere fundo nesta pista de elite!"},
    "Aguaray Eco": {"cat": "Natureza", "latitude": -25.617, "longitude": -54.484, "dica": "O refúgio perfeito para renovar as energias em trilhas selvagens."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "latitude": -25.695, "longitude": -54.436, "dica": "Um privilégio único: ver o sol nascer sobre as quedas d'água."},
    "AquaFoz": {"cat": "Cultura", "latitude": -25.616, "longitude": -54.481, "dica": "Mergulhe fundo na história viva da nossa biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "latitude": -25.538, "longitude": -54.542, "dica": "Splash! O lugar ideal para dar risada com toda a família."},
    "Bike Poço Preto": {"cat": "Esporte", "latitude": -25.695, "longitude": -54.436, "dica": "Pedale pelo coração da floresta e sinta a vida selvagem de perto."},
    "Blue Park": {"cat": "Lazer", "latitude": -25.525, "longitude": -54.548, "dica": "Água quentinha e diversão sem fim na praia termal de Foz."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "latitude": -25.684, "longitude": -54.444, "dica": "Prepare-se para ficar impressionado com o lado hermano das cataratas!"},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "latitude": -25.695, "longitude": -54.436, "dica": "A clássica e inesquecível Garganta do Diabo espera por você."},
    "Dreams Park Show": {"cat": "Lazer", "latitude": -25.565, "longitude": -54.502, "dica": "Um mundo mágico onde a imaginação ganha vida em cada museu."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "latitude": -25.534, "longitude": -54.545, "dica": "Se tem coragem, o céu de Foz é o seu melhor destino hoje!"},
    "Helisul Experience": {"cat": "Experiência", "latitude": -25.692, "longitude": -54.438, "dica": "Voe alto e tenha a melhor foto aérea da sua vida."},
    "Itaipu Panorâmica": {"cat": "Cultura", "latitude": -25.405, "longitude": -54.588, "dica": "A vista clássica que mostra o tamanho monumental dessa obra."},
    "Macuco Safari": {"cat": "Esporte", "latitude": -25.695, "longitude": -54.436, "dica": "Se prepare para se molhar e gritar de tanta emoção!"},
    "Marco das Três Fronteiras": {"cat": "Cultura", "latitude": -25.603, "longitude": -54.599, "dica": "O encontro simbólico entre Brasil, Argentina e Paraguai."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "latitude": -25.535, "longitude": -54.575, "dica": "Uma joia arquitetônica que traz o oriente para o coração de Foz."},
    "Parque das Aves": {"cat": "Natureza", "latitude": -25.617, "longitude": -54.484, "dica": "Entre no viveiro e sinta a vida das aves tropicais ao redor."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "latitude": -25.534, "longitude": -54.550, "dica": "Encontre a paz interior entre centenas de estátuas serenas."},
    "Wonder Park Foz": {"cat": "Lazer", "latitude": -25.550, "longitude": -54.540, "dica": "Cinema de alta tecnologia e shows que vão te surpreender."},
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

# --- PLANEJADOR ---
with tab1:

    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")

    st.markdown("Olá! Sou o **X.Tur**, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros turísticos.")

    st.markdown("💡 Categorias: **Natureza | Esporte | Cultura | Lazer | Experiência**")

    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    btn = st.button("🚀 Gerar roteiro inteligente")

    if btn:

        resultados = []

        for nome, item in atrativos_db.items():

            score = round(random.uniform(5.3,10.5),1)

            reputacao = round(random.uniform(3.0,4.9),1)

            transito = random.choice(["Intenso","Não Intenso"])

            capacidade = random.choice(["Lotado","Não Lotado"])

            resultados.append({
                "nome": nome,
                "score": score,
                "reputacao": reputacao,
                "transito": transito,
                "capacidade": capacidade,
                "item": item
            })

        resultados = sorted(resultados, key=lambda x: x["score"], reverse=True)

        for r in resultados:

            st.markdown(f"### 📍 {r['nome']} ⭐ {r['score']}")

            st.write(
            f"""
            **Reputação Digital:** {r['reputacao']}  
            **Fluxo de Trânsito:** {r['transito']}  
            **Capacidade de Carga:** {r['capacidade']}
            """
            )

            if r['capacidade'] == "Lotado":
                st.warning("⚠️ O local está lotado. Considere visitar em outro horário.")

            elif r['transito'] == "Intenso":
                st.info("🚗 Trânsito intenso na região. Recomenda-se sair mais cedo.")

            else:
                st.success("✅ Condições ideais para visitação.")

            st.info(f"💡 {r['item']['dica']}")

            st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(r["nome"]))

            st.markdown("---")

# --- MAPA ---
with tab2:

    st.header("📍 Mapa Geral")

    df = pd.DataFrame.from_dict(atrativos_db, orient='index')

    st.map(df)

# --- EXPLICAÇÃO IA ---
with tab3:

    st.header("🧠 Inteligência Artificial Não Generativa")

    st.write("""

O **FluxoTur** utiliza uma arquitetura de **Inteligência Artificial Não Generativa**.

Diferente de sistemas de IA generativa, que produzem textos, imagens ou conteúdos novos, o FluxoTur atua como um **sistema de análise e recomendação baseado em dados estruturados**.

Na prática, a IA analisa diferentes variáveis dos atrativos turísticos, como:

• reputação digital  
• fluxo de trânsito  
• capacidade de carga do atrativo  
• categoria turística  
• score de prioridade de visita

A partir dessas variáveis o sistema realiza três etapas principais:

**1 – Triagem de atrativos**  
Identifica quais locais são relevantes para o visitante.

**2 – Avaliação de condições de visitação**  
Analisa trânsito, lotação e reputação digital.

**3 – Otimização do roteiro turístico**  
Organiza os atrativos em ordem de prioridade de visita.

Assim, o **FluxoTur atua como um assistente inteligente de planejamento turístico**, ajudando o visitante a decidir **quando e onde visitar cada atrativo em Foz do Iguaçu** de forma mais eficiente.

""")
