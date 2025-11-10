import streamlit as st
import pandas as pd
import numpy as np

# --- 1. CONFIGURAÇÃO DE ESTILO E PÁGINA ---

# CSS para tentar adicionar uma imagem de fundo e melhorar o estilo
# ATENÇÃO: Carregar fundos de arquivos locais (fundo_bonito.jpg) é instável no Streamlit Cloud.
# O código abaixo prioriza o estilo geral.
st.markdown("""
    <style>
    /* Estilo para a barra lateral */
    .css-1d391kg {{
        background-color: #2e7a3d !important; /* Um tom de verde mais escuro */
        color: white;
    }}
    /* Estilo para o título principal */
    .stApp > header {{
        background-color: transparent;
    }}
    /* Centralizar o mapa para melhor visualização */
    .stMap {{
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Gestão de E-Lixo Barretos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DADOS SIMULADOS DE PEVs EM BARRETOS (COORDENADAS APROXIMADAS) ---

# Coordenadas do centro aproximado de Barretos (para centralizar o mapa)
BARRETOS_CENTER_LAT = -20.5540
BARRETOS_CENTER_LON = -48.5700

PEVS_DATA = {
    'nome': [
        "PEV Prefeitura (Centro)",
        "PEV North Shopping",
        "PEV Região California",
        "PEV Residencial City Barretos",
        "PEV UPA"
    ],
    'lat': [
        -20.5580,  # Centro (Próximo à Prefeitura)
        -20.5400,  # Shopping (Mais ao norte)
        -20.5750,  # Mais ao sul
        -20.5650,  # Oeste
        -20.5500   # Leste
    ],
    'lon': [
        -48.5740,
        -48.5780,
        -48.5700,
        -48.5850,
        -48.5600
    ],
    'status': [
        "✅ Livre",
        "⚠️ Coleta Urgente",
        "✅ Livre",
        "⚠️ Coleta Urgente",
        "✅ Livre"
    ]
}

# Cria o DataFrame para o mapa
df_pevs = pd.DataFrame(PEVS_DATA)

# --- 3. FUNÇÃO PRINCIPAL DA INTERFACE ---

def app_principal():
    st.title("♻️ E-Lixo Barretos: Mapa Comunitário")
    st.markdown("Uma plataforma para descarte consciente e monitoramento de eletrônicos.")
    st.markdown("---")
    
    # Simulação da Geolocalização Ativa
    st.sidebar.info("📡 Geolocalização Ativa: Verifique a distância em tempo real.", icon="🧭")

    # Criação das Abas
    tab1, tab2 = st.tabs(["Localizar Ponto de Descarte (PEV)", "Monitor de Bem-Estar Digital"])

    # --- ABA 1: Logística (Mapeamento) ---
    with tab1:
        st.header("📍 Pontos de Entrega Voluntária (PEVs) em Barretos")
        
        # Cria e exibe o mapa
        st.map(df_pevs, latitude='lat', longitude='lon', zoom=12)
        
        # Tabela com detalhes dos PEVs (para visualização de status)
        st.subheader("Status Detalhado dos Pontos de Coleta")
        
        # Estiliza a tabela com cores baseadas no status
        def color_status(val):
            if 'Urgente' in val:
                color = 'background-color: #f8d7da; color: #721c24;' # Vermelho claro
            elif 'Livre' in val:
                color = 'background-color: #d4edda; color: #155724;' # Verde claro
            else:
                color = ''
            return color

        st.dataframe(
            df_pevs.style.applymap(color_status, subset=['status']),
            use_container_width=True,
            hide_index=True
        )

        # Simulação do Fluxo de Crowdsourcing
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Botão para iniciar o fluxo de Prova Fotográfica
            if st.button("Reportar Status de um PEV", type="primary"):
                st.session_state.report_flow = True

        with col2:
            st.markdown(
                """
                *Use este botão para informar a situação do ponto (ex: lotado, coleta necessária)
                e nos ajudar a manter a logística da cidade otimizada.*
                """
            )
        
        # Fluxo de Prova Fotográfica (simulação de upload)
        if 'report_flow' in st.session_state and st.session_state.report_flow:
            st.markdown("---")
            st.subheader("📷 Prova Fotográfica")
            st.warning("Selecione uma foto que mostre a situação atual do PEV. (Simulação)")
            
            # Dropdown para selecionar o PEV (necessário para o relatório)
            selected_pev = st.selectbox(
                "Qual PEV você está reportando?",
                options=df_pevs['nome']
            )

            # Campo de upload de arquivo
            uploaded_file = st.file_uploader("Carregar Imagem", type=['png', 'jpg', 'jpeg'])
            
            if uploaded_file is not None and st.button("ENVIAR PROVA E ATUALIZAR STATUS"):
                st.success(f"Obrigado! Relatório para '{selected_pev}' enviado com sucesso. A coleta será agendada.")
                st.session_state.report_flow = False # Fecha o fluxo após envio
                st.experimental_rerun()


    # --- ABA 2: Higiene Digital (Foco no Usuário) ---
    with tab2:
        st.header("🧘 Seu Bem-Estar e o Descarte")
        st.markdown("O uso excessivo de eletrônicos está ligado à geração de e-lixo e à sua saúde. Monitore seu uso:")
        
        # Métricas de uso amigáveis
        col_m1, col_m2, col_m3 = st.columns(3)
        
        col_m1.metric(label="Tempo de Tela (Média Diária)", value="5h 30m", delta="-30m vs. Semana Passada")
        col_m2.metric(label="Alerta de Postura", value="✅ OK", delta="0 Alertas Hoje")
        col_m3.metric(label="Horas de Sono (Média)", value="7h 15m", delta="Melhora de 15m")
        
        st.markdown("---")
        st.subheader("📱 Dicas Rápidas para o Descarte")
        st.write("""
        * **Não Jogue no Lixo Comum:** Pilhas e eletrônicos possuem metais pesados que contaminam o solo e a água.
        * **Apague seus Dados:** Sempre faça um reset de fábrica em celulares e computadores antes de descartar.
        * **Aproveite a Vida Útil:** Tente consertar ou doar antes de descartar!
        """)


if __name__ == "__main__":
    app_principal()