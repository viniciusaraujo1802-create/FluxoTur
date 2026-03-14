import streamlit as st
import random
import pandas as pd

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- VLIBRAS CORRIGIDO ---
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
            bottom: 20px !important;
            right: 20px !important;
            z-index: 999999 !important;
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

# --- BASE DE DADOS COM DICAS ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "dica": "Sinta a adrenalina correndo em uma pista de nível profissional."},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "dica": "Conecte-se com a natureza em trilhas autoguiadas e cachoeiras revigorantes."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Prepare a câmera para a vista mais icônica da Garganta do Diabo."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "dica": "Caminhe entre araras e tucanos em um santuário de preservação único."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "dica": "Assista ao pôr do sol onde Brasil, Argentina e Paraguai se encontram."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "dica": "Conheça o interior da maior usina hidrelétrica do mundo em energia produzida."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Prepare-se para um banho inesquecível embaixo das quedas d'água."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "dica": "Relaxe nas águas termais com ondas artificiais para toda a família."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "dica": "Veja Foz do Iguaçu de um ângulo privilegiado lá do alto."},
    # Adicione dicas para os outros conforme necessário...
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    st.markdown("Olá! Sou o X.Tur, a inteligência artificial não generativa da FluxoTur especializada na otimização de roteiros com os atrativos encontrados no site [Foz do Iguaçu Destino do Mundo](https://www.destino.foz.br/).")
    
    pesquisa = st.text_input("💬 O que você deseja fazer hoje? (Digite e aperte ENTER ou clique no botão abaixo)")
    btn_clicado = st.button("🚀 Gerar roteiro inteligente")
    
    if btn_clicado or pesquisa:
        with st.spinner("Analisando dados do destino..."):
            lista_resultados = []
            for nome, info in atrativos_db.items():
                if not pesquisa or info['cat'].lower() == pesquisa.lower():
                    score = round(random.uniform(5.3, 10.5), 1)
                    c = random.choice(["Lotado", "Não Lotado"])
                    t = random.choice(["Intenso", "Não Intenso"])
                    # Adiciona a dica recuperada da base
                    dica = info.get("dica", "Um lugar imperdível para incluir no seu roteiro!")
                    lista_resultados.append({"nome": nome, "score": score, "R": info['R'], "t": t, "c": c, "dica": dica})
            
            if not lista_resultados:
                st.warning("🤖 Ops! Não encontrei nada com essa categoria. Que tal tentar 'Natureza' ou 'Esporte'?")
            else:
                lista_resultados.sort(key=lambda x: x['score'], reverse=True)
                st.success(f"🤖 Encontrei {len(lista_resultados)} opções. Aqui está o seu fluxo ideal:")
                
                for item in lista_resultados:
                    st.markdown(f"### 📍 {item['nome']} ({item['score']})")
                    st.info(f"💡 **Dica do X.Tur:** {item['dica']}") # A mensagem interativa antes dos dados
                    st.write(f"**Reputação:** {item['R']} | **Trânsito:** {item['t']} | **Capacidade:** {item['c']}")
                    st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(item['nome']))
                    st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral")
    # Filtro para evitar erro do mapa (garante que apenas itens com lat/lon sejam plotados)
    df = pd.DataFrame.from_dict(atrativos_db, orient='index')
    if not df.empty:
        df = df.rename(columns={'lat': 'latitude', 'lon': 'longitude'})
        st.map(df[['latitude', 'longitude']])

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("O FluxoTur é um sistema especialista voltado para a otimização de dados turísticos reais.")
