import streamlit as st
import random

st.set_page_config(page_title="FLUXOTUR", layout="wide")

st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico – Foz do Iguaçu")

# ----------------------------
# BASE COMPLETA – 33 ATRATIVOS
# ----------------------------

atrativos = {
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

# ----------------------------
# FUNÇÕES DA IA
# ----------------------------

def gerar_variaveis():
    dados = {}
    for nome, descricao in atrativos.items():
        dados[nome] = {
            "capacidade": random.choice(["lotado", "não lotado"]),
            "transito": random.choice(["congestionado", "não congestionado"]),
            "reputacao": round(random.uniform(4.3, 4.9),1),
            "descricao": descricao
        }
    return dados


def calcular_score(d):
    score = 0
    score += 3 if d["capacidade"] == "não lotado" else -2
    score += 3 if d["transito"] == "não congestionado" else -2
    score += d["reputacao"]
    return score


# ----------------------------
# INTERFACE
# ----------------------------

st.sidebar.header("Configuração da Rota")
limite_score = st.sidebar.slider("Score mínimo para recomendação", 0, 15, 5)

if st.button("🚀 Gerar Rota Inteligente"):

    dados = gerar_variaveis()
    ranking = []

    for nome, info in dados.items():
        score = calcular_score(info)
        ranking.append((nome, score, info))

    ranking.sort(key=lambda x: x[1], reverse=True)

    st.success("Rota otimizada para menor congestionamento")

    for nome, score, info in ranking:
        if score >= limite_score:
            with st.container():
                st.markdown(f"### {nome}")
                st.write(f"Score: {round(score,2)}")
                st.write(f"Capacidade: {info['capacidade']}")
                st.write(f"Fluxo de Trânsito: {info['transito']}")
                st.write(f"Reputação Digital: {info['reputacao']}")
                st.write(f"O que fazer: {info['descricao']}")
                st.markdown("---")
