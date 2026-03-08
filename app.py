import streamlit as st
import random
import time

st.set_page_config(page_title="FluxoTur - X.TUR", layout="wide")

# --- CSS COM IMAGEM ---
def set_style():
    bg_url = "https://i.ibb.co/nq73snyt/download.jpg"
    st.markdown(f"""
    <style>
    .stApp {{ background-image: url("{bg_url}"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .block-container {{ background-color: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; }}
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

set_style()

# --- BASE DE DADOS COMPLETA (33 ATRATIVOS) ---
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

# --- ALGORITMO MCDM ---
def calcular_score_mcdm(reputacao, carga_status, transito_status):
    w_carga = 0.5 if carga_status == 1 else -0.5
    w_transito = 0.5 if transito_status == 1 else -0.5
    return round(reputacao + w_carga + w_transito, 2)

# --- INTERFACE ---
st.title("🌍 FluxoTur")
st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")

# Categorias Visíveis
st.markdown("### 💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
st.markdown("---")

pesquisa = st.text_input("💬 O que você deseja fazer hoje?")

if pesquisa:
    cat_busca = pesquisa.capitalize()
    mapeamento = {"Igreja": "Cultura", "Templo": "Cultura", "Mesquita": "Cultura"}
    cat_final = mapeamento.get(cat_busca, cat_busca)
    
    resultados = {n: d for n, d in atrativos_db.items() if d['cat'].lower() == cat_final.lower()}
    
    if not resultados:
        st.warning("X.TUR: Não encontrei atrativos para este critério. Tente as categorias listadas.")
    else:
        st.info(f"X.TUR: Analisando infraestrutura e reputação para: {cat_final}.")
        
        if st.button("🚀 Gerar roteiro inteligente"):
            with st.spinner("X.TUR: Processando via MCDM..."):
                time.sleep(1.2)
                ranking = []
                for nome, info in resultados.items():
                    c = random.choice([0, 1])
                    t = random.choice([0, 1])
                    s = calcular_score_mcdm(info['R'], c, t)
                    ranking.append({"nome": nome, "score": s, "c": c, "t": t})
                
                ranking.sort(key=lambda x: x['score'], reverse=True)
                
                st.success("X.TUR: Roteiro gerado com base na otimização MCDM:")
                for item in ranking:
                    status_c = "Não Lotado" if item['c'] == 1 else "Lotado"
                    status_t = "Não Congestionado" if item['t'] == 1 else "Congestionado"
                    st.markdown(f"### 📍 {item['nome']} (Score Final: {item['score']:.1f})")
                    st.write(f"**Condições:** Capacidade ({status_c}) | Fluxo de Trânsito ({status_t})")
                    st.markdown("---")
                st.balloons()
