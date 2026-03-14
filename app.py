import streamlit.components.v1 as components

# --- VLIBRAS (MODO COMPONENTES) ---
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
        [vw] { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 99999999 !important; }
    </style>
    """
    # Usamos o components.html para forçar a renderização fora da "sandbox" do markdown
    components.html(vlibras_html, height=100)

# Chame a função logo após o set_page_config
injetar_vlibras()
