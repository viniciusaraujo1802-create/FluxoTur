import streamlit as st
import random
import pandas as pd

# Configuração inicial
st.set_page_config(page_title="FLUXOTUR - Pesquisa Científica", layout="wide")

# --- BASE DE DADOS (33 Atrativos) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": "Esporte, kart indoor, profissional.",
    "Aguaray Eco": "Natureza, trilha, cachoeiras.",
    "Amanhecer nas Cataratas": "Natureza, experiência, exclusivo, sol.",
    "AquaFoz": "Cultura, aquário, espécies.",
    "Aquamania": "Lazer, parque aquático, toboáguas.",
    "Bike Poço Preto": "Esporte, cicloturismo, natureza.",
    "Blue Park": "Lazer, parque aquático, termal.",
    "Cataratas del Iguazú – Argentina": "Natureza, turismo, Argentina.",
    "Cataratas do Iguaçu – Brasil": "Natureza, turismo, principal.",
    "Céu das Cataratas": "Experiência, aéreo, exclusivo.",
    "Circuito São João": "Cultura, passeio, regional.",
    "Dreams Park Show": "Lazer, museu, cera, atrações.",
    "Falls Bike Tour": "Esporte, bicicleta, guiado.",
    "Fly Foz – Paraquedismo": "Esporte, adrenalina, paraquedismo.",
    "Helisul Experience": "Experiência, helicóptero, Cataratas.",
    "Iguassu By Bike": "Esporte, cicloturismo, urbano.",
    "Iguassu River Tour": "Natureza, barco, Rio Iguaçu.",
    "Iguassu Secret Falls": "Natureza, expedição, cachoeiras.",
    "Iguazu Wellness": "Relaxamento, yoga, bem-estar.",
    "Itaipu Especial": "Cultura, técnico, usina.",
    "Itaipu Iluminada": "Cultura, show, luzes.",
    "Itaipu Panorâmica": "Cultura, visita, usina.",
    "Itaipu Refúgio Biológico": "Natureza, conservação, ambiental.",
    "Kattamaram": "Lazer, barco, Lago de Itaipu.",
    "Macuco Safari": "Esporte, adrenalina, barco.",
    "Marco das Três Fronteiras": "Cultura, encontro, três países.",
    "Mesquita Omar Ibn Al-Khattab": "Cultura, arquitetura, religiosa.",
    "Parque das Aves": "Natureza, conservação, aves.",
    "Pôr do Sol nas Cataratas": "Natureza, experiência, pôr do sol.",
    "Templo Budista Chen Tien": "Cultura, templo, budismo.",
    "Turismo Itaipu": "Cultura, oficial, visita.",
    "Wonder Park Foz": "Lazer, interativo, complexo.",
    "Yup Star – Roda Gigante": "Lazer, roda gigante, vista."
}

# --- FUNÇÃO DO ALGORITMO MCDM ---
def calcular_score_mcdm(reputacao, cap_carga, transito):
    w1 = 3 if cap_carga == "Não Lotado" else -2
    w2 = 3 if transito == "Não Congestionado" else -2
    return reputacao + w1 + w2

# --- INTERFACE ---
st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico – Foz do Iguaçu")

# A INTERAÇÃO (Busca Inteligente)
pesquisa = st.text_input("💬 O que você deseja fazer hoje? (ex: esporte, natureza, cultura)")

# Filtro dos 33 atrativos
lista_filtrada = {n: d for n, d in atrativos_db.items() if pesquisa.lower() in d.lower() or pesquisa == ""}

tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 Gerador de Rota", "🧪 Simulador de Impacto", "🚗 Diagnóstico de Mobilidade", "📚 Fundamentação Teórica"
])

with tab1:
    st.header("Assistente de Roteiro Inteligente")
    if pesquisa: st.info(f"Mostrando resultados filtrados para: {pesquisa}")
    
    if st.button("🚀 Gerar Rota Otimizada"):
        ranking = []
        for nome, desc in lista_filtrada.items():
            cap = random.choice(["Lotado", "Não Lotado"])
            tra = random.choice(["Congestionado", "Não Congestionado"])
            rep = round(random.uniform(4.3, 4.9), 1)
            score = calcular_score_mcdm(rep, cap, tra)
            ranking.append({"Local": nome, "Score": score, "Capacidade": cap, "Trânsito": tra, "Info": desc})
        
        for item in sorted(ranking, key=lambda x: x['Score'], reverse=True):
            with st.expander(f"{item['Local']} - Score: {item['Score']:.1f}"):
                st.write(f"**Status:** {item['Capacidade']} | **Tráfego:** {item['Trânsito']}")
                st.write(f"**Descrição:** {item['Info']}")

with tab2:
    st.header("Simulador de Sensibilidade")
    s_rep = st.slider("Reputação Digital (R)", 4.3, 4.9, 4.6, step=0.1)
    s_cap = st.select_slider("Capacidade (C)", options=["Lotado", "Não Lotado"])
    s_tra = st.select_slider("Trânsito (T)", options=["Congestionado", "Não Congestionado"])
    st.metric("Score Final (S)", f"{calcular_score_mcdm(s_rep, s_cap, s_tra):.1f}")

with tab3:
    st.header("Diagnóstico de Mobilidade")
    tempo_normal = st.number_input("Tempo normal (min)", 10, 60, 20)
    tempo_gps = st.number_input("Tempo atual (min)", 10, 100, 22)
    if tempo_gps > (tempo_normal * 1.2): st.error("Status: Congestionado")
    else: st.success("Status: Fluido")

with tab4:
    st.header("Metodologia Científica")
    st.markdown("$$S = R + (C \\times w_1) + (T \\times w_2)$$")
