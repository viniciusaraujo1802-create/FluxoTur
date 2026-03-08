import streamlit as st
import random

# Configuração inicial
st.set_page_config(page_title="FLUXOTUR", layout="wide")

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
    "Iguazu Wellness": "Experiência, yoga, bem-estar.",
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

# --- FUNÇÃO DE MAPEAMENTO INTELIGENTE (NLP) ---
def extrair_categoria(frase):
    frase = frase.lower()
    if any(x in frase for x in ["natureza", "trilha", "cachoeira", "eco", "parque", "selva", "árvore", "verde", "rio", "água", "refúgio", "biológico", "animal", "aves", "ao ar livre"]): return "Natureza"
    if any(x in frase for x in ["esporte", "kart", "bike", "bicicleta", "cicloturismo", "paraquedismo", "adrenalina", "salto", "radical", "ativo", "exercício", "pedalar"]): return "Esporte"
    if any(x in frase for x in ["cultura", "igreja", "templo", "mesquita", "história", "histórico", "técnico", "usina", "museu", "arquitetura", "religioso", "tradição", "cidade"]): return "Cultura"
    if any(x in frase for x in ["lazer", "diversão", "parque aquático", "família", "criança", "passeio", "termal", "roda gigante", "show", "barco", "cruzeiro"]): return "Lazer"
    if any(x in frase for x in ["experiência", "yoga", "wellness", "relaxar", "exclusivo", "pôr do sol", "nascer do sol", "bem-estar", "helicóptero", "vista", "panorâmica"]): return "Experiência"
    return "Geral"

# --- FUNÇÃO MCDM ---
def calcular_score_mcdm(reputacao, cap_carga, transito):
    w1 = 3 if cap_carga == "Não Lotado" else -2
    w2 = 3 if transito == "Não Congestionado" else -2
    return reputacao + w1 + w2

# --- INTERFACE ---
st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico – Foz do Iguaçu")

pesquisa = st.text_input("💬 O que você deseja fazer hoje? (Sugestões: Esporte, Natureza, Cultura, Lazer, Experiência)")

if pesquisa:
    cat = extrair_categoria(pesquisa)
    st.write(f"💬 **Consultor FluxoTur:** Entendido! Buscando por opções de **{cat}** para você:")
    lista_filtrada = {n: d for n, d in atrativos_db.items() if cat.lower() in d.lower() or cat == "Geral"}
else:
    lista_filtrada = atrativos_db

st.markdown("---")

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
