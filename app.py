import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="FLUXOTUR", layout="wide")

# --- BASE DE DADOS ---
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

def extrair_categoria(frase):
    frase = frase.lower()
    if any(x in frase for x in ["natureza", "trilha", "cachoeira", "eco", "parque", "selva", "árvore", "verde", "rio", "água", "refúgio", "biológico", "animal", "aves", "ao ar livre"]): return "Natureza"
    if any(x in frase for x in ["esporte", "kart", "bike", "bicicleta", "cicloturismo", "paraquedismo", "adrenalina", "salto", "radical", "ativo", "exercício", "pedalar"]): return "Esporte"
    if any(x in frase for x in ["cultura", "igreja", "templo", "mesquita", "história", "histórico", "técnico", "usina", "museu", "arquitetura", "religioso", "tradição", "cidade"]): return "Cultura"
    if any(x in frase for x in ["lazer", "diversão", "parque aquático", "família", "criança", "passeio", "termal", "roda gigante", "show", "barco", "cruzeiro"]): return "Lazer"
    if any(x in frase for x in ["experiência", "yoga", "wellness", "relaxar", "exclusivo", "pôr do sol", "nascer do sol", "bem-estar", "helicóptero", "vista", "panorâmica"]): return "Experiência"
    return "Geral"

# --- INTERFACE ---
st.title("🌍 FLUXOTUR")
st.subheader("Planejamento Inteligente de Roteiro Turístico – Foz do Iguaçu")

# Exibição fixa das opções
st.markdown("""
---
### 💡 Você pode buscar por:
**Natureza** | **Esporte** | **Cultura** | **Lazer** | **Experiência**
---
""")

pesquisa = st.text_input("💬 O que você deseja fazer hoje?")

if pesquisa:
    cat = extrair_categoria(pesquisa)
    st.info(f"🔍 Entendi! Estou filtrando sugestões para o seu interesse em: **{cat}**.")
    
    if st.button("🚀 Gerar Rota Otimizada"):
        with st.spinner("Buscando os melhores atrativos..."):
            lista = {n: d for n, d in atrativos_db.items() if cat.lower() in d.lower() or cat == "Geral"}
            
            st.success(f"Encontrei {len(lista)} opções ideais para você:")
            
            ranking = []
            for nome, desc in lista.items():
                score = round(random.uniform(4.0, 5.0), 1)
                cap = random.choice(["Lotado", "Não Lotado"])
                tra = random.choice(["Congestionado", "Não Congestionado"])
                ranking.append({"nome": nome, "score": score, "cap": cap, "tra": tra, "desc": desc})
            
            for item in sorted(ranking, key=lambda x: x['score'], reverse=True):
                st.markdown(f"### {item['nome']} (Score: {item['score']:.1f})")
                st.write(f"**Status:** {item['cap']} | **Tráfego:** {item['tra']}")
                st.write(f"**Descrição:** {item['desc']}")
                st.markdown("---")
