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
        [vw] { position: fixed !important; bottom: 20px !important; right: 20px !important; z-index: 999999 !important; }
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

# --- BASE DE DADOS (33 ATRATIVOS) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "lat": -25.534, "lon": -54.545, "dica": "Pista profissional."},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "lat": -25.617, "lon": -54.484, "dica": "Trilhas e natureza."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Vista exclusiva."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "lat": -25.616, "lon": -54.481, "dica": "Biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "lat": -25.538, "lon": -54.542, "dica": "Diversão aquática."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "lat": -25.695, "lon": -54.436, "dica": "Bike na floresta."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "lat": -25.525, "lon": -54.548, "dica": "Águas termais."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "lat": -25.684, "lon": -54.444, "dica": "Beleza argentina."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Garganta do Diabo."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "lat": -25.695, "lon": -54.436, "dica": "Gastronomia."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "lat": -25.510, "lon": -54.500, "dica": "Raízes locais."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "lat": -25.565, "lon": -54.502, "dica": "Museus temáticos."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "lat": -25.695, "lon": -54.436, "dica": "Pedal nas quedas."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "lat": -25.534, "lon": -54.545, "dica": "Salto de paraquedas."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "lat": -25.692, "lon": -54.438, "dica": "Voo panorâmico."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "lat": -25.550, "lon": -54.580, "dica": "Passeio guiado."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "lat": -25.690, "lon": -54.435, "dica": "Tour pelo rio."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "lat": -25.550, "lon": -54.550, "dica": "Cachoeiras ocultas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "lat": -25.560, "lon": -54.520, "dica": "Bem-estar."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "lat": -25.405, "lon": -54.588, "dica": "Visita técnica."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Usina à noite."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "lat": -25.405, "lon": -54.588, "dica": "Vista da Itaipu."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "lat": -25.410, "lon": -54.550, "dica": "Fauna e flora."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "lat": -25.405, "lon": -54.588, "dica": "Passeio de barco."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Banho radical."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "lat": -25.603, "lon": -54.599, "dica": "Três países."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "lat": -25.535, "lon": -54.575, "dica": "Arquitetura islâmica."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "lat": -25.617, "lon": -54.484, "dica": "Aves tropicais."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "lat": -25.695, "lon": -54.436, "dica": "Pôr do sol."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "lat": -25.534, "lon": -54.550, "dica": "Paz e reflexão."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "lat": -25.405, "lon": -54.588, "dica": "Tudo sobre Itaipu."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "lat": -25.550, "lon": -54.540, "dica": "Cinema e shows."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "lat": -25.600, "lon": -54.600, "dica": "Vista panorâmica."}
}

# --- INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🚀 Planejador FluxoTur", "📍 Mapa Geral", "🧠 Entenda o FluxoTur"])

with tab1:
    st.title("🌍 FluxoTur")
    st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
    st.markdown("Olá! Sou o X.Tur, a IA não generativa da FluxoTur.")
    
    pesquisa = st.text_input("💬 O que você deseja fazer hoje?")
    btn_clicado = st.button("🚀 Gerar roteiro inteligente")
    
    if btn_clicado or pesquisa:
        with st.spinner("Analisando dados..."):
            lista_resultados = []
            for nome, info in atrativos_db.items():
                if not pesquisa or info['cat'].lower() == pesquisa.lower():
                    score = round(random.uniform(5.3, 10.5), 1)
                    c = random.choice(["Lotado", "Não Lotado"])
                    t = random.choice(["Intenso", "Não Intenso"])
                    lista_resultados.append({"nome": nome, "score": score, "R": info['R'], "t": t, "c": c, "dica": info['dica']})
            
            if not lista_resultados:
                st.warning("🤖 Ops! Não encontrei nada.")
            else:
                lista_resultados.sort(key=lambda x: x['score'], reverse=True)
                st.success(f"🤖 Encontrei {len(lista_resultados)} opções:")
                for item in lista_resultados:
                    st.markdown(f"### 📍 {item['nome']} ({item['score']})")
                    st.info(f"💡 Dica: {item['dica']}")
                    st.write(f"**Reputação:** {item['R']} | **Trânsito:** {item['t']} | **Capacidade:** {item['c']}")
                    st.link_button("📍 Abrir no Google Maps", gerar_link_mapas(item['nome']))
                    st.markdown("---")

with tab2:
    st.header("📍 Mapa Geral")
    df = pd.DataFrame.from_dict(atrativos_db, orient='index')
    # Renomeando corretamente para evitar o erro do st.map
    df = df.rename(columns={'lat': 'latitude', 'lon': 'longitude'})
    st.map(df)

with tab3:
    st.header("🧠 Inteligência Artificial Não Generativa")
    st.write("O FluxoTur é um sistema especialista em dados turísticos de Foz do Iguaçu.")
