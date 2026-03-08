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
    "Kartódromo - Adrena Kart": {"cat": "Esporte", "R": 4.5, "desc": "Kart indoor de alta velocidade."},
    "Aguaray Eco": {"cat": "Natureza", "R": 4.8, "desc": "Trilhas em meio à mata e cachoeiras."},
    "Amanhecer nas Cataratas": {"cat": "Experiência", "R": 4.9, "desc": "Experiência exclusiva ao nascer do sol."},
    "AquaFoz": {"cat": "Cultura", "R": 4.6, "desc": "Aquário com biodiversidade local."},
    "Aquamania": {"cat": "Lazer", "R": 4.4, "desc": "Parque aquático com toboáguas."},
    "Bike Poço Preto": {"cat": "Esporte", "R": 4.7, "desc": "Cicloturismo em trilhas no Parque Nacional."},
    "Blue Park": {"cat": "Lazer", "R": 4.5, "desc": "Parque aquático termal com praia artificial."},
    "Cataratas del Iguazú – Argentina": {"cat": "Natureza", "R": 4.9, "desc": "Vistas panorâmicas e trilhas argentinas."},
    "Cataratas do Iguaçu – Brasil": {"cat": "Natureza", "R": 4.9, "desc": "A clássica passarela das quedas d'água."},
    "Céu das Cataratas": {"cat": "Experiência", "R": 4.8, "desc": "Vista aérea e jantar exclusivo."},
    "Circuito São João": {"cat": "Cultura", "R": 4.3, "desc": "Passeios rurais e cultura regional."},
    "Dreams Park Show": {"cat": "Lazer", "R": 4.5, "desc": "Museu de cera e atrações interativas."},
    "Falls Bike Tour": {"cat": "Esporte", "R": 4.6, "desc": "Passeio de bike guiado pelos atrativos."},
    "Fly Foz – Paraquedismo": {"cat": "Esporte", "R": 4.9, "desc": "Salto duplo de paraquedas."},
    "Helisul Experience": {"cat": "Experiência", "R": 4.9, "desc": "Voo de helicóptero sobre as Cataratas."},
    "Iguassu By Bike": {"cat": "Esporte", "R": 4.5, "desc": "Mobilidade urbana sustentável."},
    "Iguassu River Tour": {"cat": "Natureza", "R": 4.7, "desc": "Navegação cênica pelo Rio Iguaçu."},
    "Iguassu Secret Falls": {"cat": "Natureza", "R": 4.8, "desc": "Expedição por cachoeiras escondidas."},
    "Iguazu Wellness": {"cat": "Experiência", "R": 4.7, "desc": "Yoga e terapias de bem-estar."},
    "Itaipu Especial": {"cat": "Cultura", "R": 4.8, "desc": "Tour técnico pela barragem de Itaipu."},
    "Itaipu Iluminada": {"cat": "Cultura", "R": 4.7, "desc": "Show de luzes na usina hidrelétrica."},
    "Itaipu Panorâmica": {"cat": "Cultura", "R": 4.6, "desc": "Vista do alto da maior usina do mundo."},
    "Itaipu Refúgio Biológico": {"cat": "Natureza", "R": 4.7, "desc": "Preservação e animais nativos."},
    "Kattamaram": {"cat": "Lazer", "R": 4.5, "desc": "Passeio de barco no Lago de Itaipu."},
    "Macuco Safari": {"cat": "Esporte", "R": 4.9, "desc": "Aventura radical embaixo das quedas."},
    "Marco das Três Fronteiras": {"cat": "Cultura", "R": 4.8, "desc": "Encontro do Brasil, Argentina e Paraguai."},
    "Mesquita Omar Ibn Al-Khattab": {"cat": "Cultura", "R": 4.7, "desc": "Arquitetura islâmica e cultura religiosa."},
    "Parque das Aves": {"cat": "Natureza", "R": 4.9, "desc": "Imersão com aves da Mata Atlântica."},
    "Pôr do Sol nas Cataratas": {"cat": "Experiência", "R": 4.9, "desc": "Final de tarde com vista privilegiada."},
    "Templo Budista Chen Tien": {"cat": "Cultura", "R": 4.8, "desc": "Jardins zen e contemplação religiosa."},
    "Turismo Itaipu": {"cat": "Cultura", "R": 4.7, "desc": "Complexo completo da usina."},
    "Wonder Park Foz": {"cat": "Lazer", "R": 4.6, "desc": "Museu de carros e show de luzes."},
    "Yup Star – Roda Gigante": {"cat": "Lazer", "R": 4.4, "desc": "Vista panorâmica da tríplice fronteira."}
}

# --- ALGORITMO MCDM ---
def calcular_score_mcdm(reputacao, carga_status, transito_status):
    w_carga = 0.5 if carga_status == 1 else -0.5
    w_transito = 0.5 if transito_status == 1 else -0.5
    return round(reputacao + w_carga + w_transito, 2)

# --- INTERFACE ---
st.title("🌍 FluxoTur")
st.subheader("Planejamento Inteligente de Roteiro Turístico - Foz do Iguaçu")
st.markdown("### 💡 Categorias: **Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**")
st.markdown("---")

pesquisa = st.text_input("💬 O que você deseja fazer hoje?")

if pesquisa:
    cat_final = pesquisa.capitalize()
    mapeamento = {"Igreja": "Cultura", "Templo": "Cultura", "Mesquita": "Cultura"}
    cat_final = mapeamento.get(cat_final, cat_final)
    
    resultados = {n: d for n, d in atrativos_db.items() if d['cat'].lower() == cat_final.lower()}
    
    if not resultados:
        st.warning("X.TUR: Não encontrei atrativos para este critério.")
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
                    ranking.append({"nome": nome, "score": s, "c": c, "t": t, "R": info['R'], "desc": info['desc']})
                
                ranking.sort(key=lambda x: x['score'], reverse=True)
                
                st.success("X.TUR: Roteiro gerado com base na otimização MCDM:")
                for item in ranking:
                    status_c = "Não Lotado" if item['c'] == 1 else "Lotado"
                    status_t = "Não Congestionado" if item['t'] == 1 else "Congestionado"
                    st.markdown(f"### 📍 {item['nome']} (Score Final: {item['score']:.1f})")
                    st.write(f"**O que fazer:** {item['desc']}")
                    st.write(f"**Reputação Digital (R):** {item['R']} | **Condições:** {status_c} | {status_t}")
                    st.markdown("---")
                st.balloons()
