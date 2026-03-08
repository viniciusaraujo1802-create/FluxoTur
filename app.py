import streamlit as st
import random
import pandas as pd

# Configuração inicial
st.set_page_config(page_title="FLUXOTUR - Pesquisa Científica", layout="wide")

# --- BASE DE DADOS (Seus 33 Atrativos) ---
atrativos_db = {
    "Kartódromo - Adrena Kart": "Kart indoor com pista profissional.",
    "Aguaray Eco": "Trilha ecológica com cachoeiras.",
    "Amanhecer nas Cataratas": "Experiência exclusiva ao nascer do sol.",
    "AquaFoz": "Aquário com espécies de água doce.",
    "Aquamania": "Parque aquático com toboáguas.",
    "Bike Poço Preto": "Cicloturismo dentro do Parque Nacional.",
    "Blue Park": "Parque aquático com praia termal.",
    "Cataratas del Iguazú – Argentina": "Lado argentino das Cataratas.",
    "Cataratas do Iguaçu – Brasil": "Principal cartão postal brasileiro.",
    "Céu das Cataratas": "Passeio aéreo exclusivo.",
    "Circuito São João": "Passeio cultural regional.",
    "Dreams Park Show": "Museu de cera, ice bar e atrações.",
    "Falls Bike Tour": "Passeios guiados de bicicleta.",
    "Fly Foz – Paraquedismo": "Salto duplo com vista panorâmica.",
    "Helisul Experience": "Voo de helicóptero sobre as Cataratas.",
    "Iguassu By Bike": "Cicloturismo urbano.",
    "Iguassu River Tour": "Passeio de barco pelo Rio Iguaçu.",
    "Iguassu Secret Falls": "Expedição para cachoeiras escondidas.",
    "Iguazu Wellness": "Yoga e experiências de bem-estar.",
    "Itaipu Especial": "Tour técnico aprofundado na usina.",
    "Itaipu Iluminada": "Show noturno de luzes na barragem.",
    "Itaipu Panorâmica": "Visita panorâmica à usina.",
    "Itaipu Refúgio Biológico": "Área de conservação ambiental.",
    "Kattamaram": "Passeio de barco no Lago de Itaipu.",
    "Macuco Safari": "Passeio de barco nas quedas.",
    "Marco das Três Fronteiras": "Encontro cultural de três países.",
    "Mesquita Omar Ibn Al-Khattab": "Arquitetura islâmica aberta à visitação.",
    "Parque das Aves": "Parque de conservação com viveiros imersivos.",
    "Pôr do Sol nas Cataratas": "Experiência exclusiva ao entardecer.",
    "Templo Budista Chen Tien": "Templo com esculturas e vista panorâmica.",
    "Turismo Itaipu": "Centro oficial de visitação.",
    "Wonder Park Foz": "Complexo com atrações interativas.",
    "Yup Star – Roda Gigante": "Roda gigante com vista panorâmica."
}

# --- FUNÇÃO DO ALGORITMO MCDM ---
def calcular_score_mcdm(reputacao, cap_carga, transito):
    # Pesos w1 e w2 conforme Quadro 1 da metodologia
    w1 = 3 if cap_carga == "Não Lotado" else -2
    w2 = 3 if transito == "Não Congestionado" else -2
    return reputacao + w1 + w2

# --- INTERFACE EM ABAS ---
st.title("🌍 FLUXOTUR")
st.markdown("##### Protótipo de Sistema de Recomendação Multicritério (MCDM)")

tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 Gerador de Rota", 
    "🧪 Simulador de Impacto", 
    "🚗 Diagnóstico de Mobilidade",
    "📚 Fundamentação Teórica"
])

# OPÇÃO 1: GERADOR DE ROTA (Seu código original melhorado)
with tab1:
    st.header("Assistente de Roteiro Inteligente")
    limite = st.slider("Score mínimo para recomendação", 0, 15, 5)
    
    if st.button("🚀 Gerar Rota Otimizada"):
        ranking = []
        for nome, desc in atrativos_db.items():
            cap = random.choice(["Lotado", "Não Lotado"])
            tra = random.choice(["Congestionado", "Não Congestionado"])
            rep = round(random.uniform(4.3, 4.9), 1)
            score = calcular_score_mcdm(rep, cap, tra)
            ranking.append({"Local": nome, "Score": score, "Capacidade": cap, "Trânsito": tra, "Rep": rep, "Info": desc})
        
        ranking_sorted = sorted(ranking, key=lambda x: x['Score'], reverse=True)
        
        for item in ranking_sorted:
            if item['Score'] >= limite:
                with st.expander(f"{item['Local']} - Score: {item['Score']:.1f}"):
                    st.write(f"**Status:** {item['Capacidade']} | **Tráfego:** {item['Trânsito']}")
                    st.write(f"**O que fazer:** {item['Info']}")

# OPÇÃO 2: SIMULADOR DE IMPACTO (Interatividade pura com a fórmula)
with tab2:
    st.header("Simulador de Sensibilidade Algorítmica")
    st.info("Altere os parâmetros para validar a resposta do Score (S) em tempo real.")
    
    c1, c2 = st.columns(2)
    with c1:
        s_rep = st.slider("Reputação Digital (R)", 4.3, 4.9, 4.6, step=0.1)
        s_cap = st.select_slider("Capacidade de Carga (C)", options=["Lotado", "Não Lotado"])
    with c2:
        s_tra = st.select_slider("Fluxo de Trânsito (T)", options=["Congestionado", "Não Congestionado"])
    
    s_final = calcular_score_mcdm(s_rep, s_cap, s_tra)
    st.metric("Score Final (S)", f"{s_final:.1f}")
    
    # Gráfico simples de barra para visualização
    st.bar_chart({"Score": [s_final]})

# OPÇÃO 3: DIAGNÓSTICO DE MOBILIDADE (Foco na tomada de decisão)
with tab3:
    st.header("Diagnóstico de Mobilidade Urbana")
    st.write("Simulação de atraso por congestionamento (T).")
    tempo_normal = st.number_input("Tempo normal de trajeto (minutos)", 10, 60, 20)
    tempo_gps = st.number_input("Tempo atual com tráfego (minutos)", 10, 100, 22)
    
    limiar = tempo_normal * 1.2
    if tempo_gps > limiar:
        st.error(f"ALERTA: Atraso de {((tempo_gps/tempo_normal)-1)*100:.1f}%. Local penalizado no ranking.")
    else:
        st.success("STATUS: Trânsito dentro da normalidade. Local bonificado.")

# OPÇÃO 4: METODOLOGIA (O coração do seu artigo)
with tab4:
    st.header("Metodologia e Modelagem Matemática")
    st.markdown(f"""
    **Questão Problema:** Como a aplicação de um algoritmo MCDM auxilia viajantes sem roteiro?
    
    **A Fórmula:**
    O Score final ($S$) é calculado como:
    $$S = R + (C \\times w_1) + (T \\times w_2)$$
    
    **Critérios de Ponderação (Quadro 1):**
    * **Ideal (Fluidez):** Peso +3
    * **Atrito (Saturação):** Peso -2
    
    **Integridade do Modelo:** O sistema utiliza simulação de cenários (Rojo, 2006) para validar a sensibilidade da lógica.
    """)
