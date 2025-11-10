import streamlit as st
import pandas as pd
import numpy as np

# --- 1. CONFIGURAÇÃO DE ESTILO E PÁGINA ---

# CSS para melhorar o estilo da interface no navegador
st.markdown("""
    <style>
    /* Estilo para a barra lateral, usando um verde mais corporativo */
    .css-1d391kg {{
        background-color: #008000 !important; /* Verde Limão/Floresta */
        color: white;
    }}
    /* Estilo para o título principal */
    .stApp > header {{
        background-color: transparent;
    }}
    /* Centralizar o mapa e aplicar bordas arredondadas */
    .stMap {{
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); /* Sombra mais destacada */
    }}
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Gestão de E-Lixo Barretos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DADOS DOS PEVs EM BARRETOS (COORDENADAS ESTIMADAS COM BASE NOS ENDEREÇOS REAIS) ---

# Coordenadas do centro aproximado de Barretos (para centralizar o mapa)
BARRETOS_CENTER_LAT = -20.5590
BARRETOS_CENTER_LON = -48.5670

PEVS_DATA = {
    'nome': [
        "PEV Leda Amendola",
        "PEV Califórnia",
        "PEV Christiano Carvalho",
        "PEV Exposição",
        "PEV Nadir Kenan",
        "PEV Santa Cecília"
    ],
    'endereco': [
        "LSA 10 - João Botacini s/nº",
        "Rua Cristiano de Carvalho nº 50",
        "Avenida João Ribeiro do Nascimento",
        "Rua Fábio Junqueira Franco nº 301",
        "Rua Rage Caiel nº 400",
        "Avenida Antônio Machado das Dores, s/nº"
    ],
    # Coordenadas estimadas para espalhar os pontos pela cidade
    'lat': [
        -20.5500,
        -20.5750,
        -20.5400,
        -20.5600,
        -20.5550,
        -20.5650
    ],
    'lon': [
        -48.5800,
        -48.5650,
        -48.5600,
        -48.5750,
        -48.5850,
        -48.5500
    ],
    'status': [
        "✅ Livre",
        "⚠️ Coleta Urgente",
        "✅ Livre",
        "⚠️ Coleta Urgente",
        "✅ Livre",
        "⚠️ Coleta Urgente"
    ]
}

# Cria o DataFrame para o mapa e a tabela
df_pevs = pd.DataFrame(PEVS_DATA)

# --- 3. FUNÇÃO DE ANÁLISE (SIMULADA) ---

def analyze_routine(routine_text):
    """Simula a análise da rotina digital com base em palavras-chave."""
    routine_text_lower = routine_text.lower()

    if not routine_text:
        return "Por favor, descreva sua rotina para que possamos analisá-la."

    # Regras de avaliação simplificadas
    if '8 horas' in routine_text_lower or '10 horas' in routine_text_lower or 'uso excessivo' in routine_text_lower or 'insônia' in routine_text_lower or 'antes de dormir' in routine_text_lower:
        return "⚠️ **Atenção:** Sua rotina sugere um tempo de tela elevado ou hábitos noturnos prejudiciais. Considere o ciclo circadiano e a regra 20-20-20 para a saúde ocular. Lembre-se, o uso excessivo leva ao descarte precoce de aparelhos."
    elif 'exercício' in routine_text_lower or 'pausas' in routine_text_lower or 'limite de tempo' in routine_text_lower or 'fora do quarto' in routine_text_lower or 'descanso' in routine_text_lower:
        return "✅ **Parabéns!** Seus hábitos parecem saudáveis e equilibrados. Manter pausas ativas e limitar o uso noturno contribui para sua saúde e para a durabilidade dos seus eletrônicos."
    else:
        return "ℹ️ **Interessante:** Sua rotina está em análise. Lembre-se de integrar pausas e limitar o uso de telas antes de dormir para maximizar seu bem-estar digital."


# --- 4. FUNÇÃO PRINCIPAL DA INTERFACE ---

def app_principal():
    st.title("♻️ E-Lixo Barretos: Mapa Comunitário")
    st.markdown("Uma plataforma para descarte consciente e monitoramento de eletrônicos na sua região.")
    st.markdown("---")
    
    # Simulação da Geolocalização Ativa (Barra Lateral)
    st.sidebar.info("📡 Geolocalização Ativa: Encontre o PEV mais próximo de você.", icon="🧭")
    st.sidebar.markdown(f"**Cidade:** Barretos, SP")

    # Criação das Abas
    tab1, tab2 = st.tabs(["Localizar Ponto de Descarte (PEV)", "Sua Saúde Digital"])

    # --- ABA 1: Logística (Mapeamento) ---
    with tab1:
        st.header("📍 Pontos de Entrega Voluntária (PEVs) em Barretos")
        
        # Cria e exibe o mapa
        st.map(df_pevs, latitude='lat', longitude='lon', zoom=12)
        
        # Tabela com detalhes dos PEVs (incluindo o endereço)
        st.subheader("Status Detalhado dos Pontos de Coleta")
        
        # Estiliza a tabela com cores baseadas no status
        def color_status(val):
            if 'Urgente' in val:
                # Cor do Streamlit: Error/Vermelho
                color = 'background-color: rgba(253, 240, 240, 0.7); color: #842029; font-weight: bold;'
            elif 'Livre' in val:
                # Cor do Streamlit: Success/Verde
                color = 'background-color: rgba(230, 255, 230, 0.7); color: #0a3622; font-weight: bold;'
            else:
                color = ''
            return color

        # Seleciona as colunas a serem exibidas na tabela
        df_display = df_pevs[['nome', 'endereco', 'status']]
        
        st.dataframe(
            df_display.style.applymap(color_status, subset=['status']),
            use_container_width=True,
            hide_index=True
        )

        # --- Fluxo de Crowdsourcing (Reporte de Status) ---
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        
        # Inicializa o estado da sessão para o fluxo de reporte
        if 'report_flow' not in st.session_state:
            st.session_state.report_flow = False
        
        with col1:
            # Botão para iniciar o fluxo de Prova Fotográfica
            if st.button("Reportar Status de um PEV", type="primary"):
                st.session_state.report_flow = True
                st.experimental_rerun() 

        with col2:
            st.markdown(
                """
                *Use este botão para informar a situação do ponto (ex: lotado, coleta necessária)
                e nos ajudar a manter a logística da cidade otimizada.*
                """
            )
        
        # Bloco de Prova Fotográfica
        if st.session_state.report_flow:
            st.markdown("### 📷 Enviar Prova Fotográfica")
            st.info("Selecione uma foto que mostre a situação atual do PEV e clique em Enviar.")
            
            selected_pev = st.selectbox(
                "Qual PEV você está reportando?",
                options=df_pevs['nome'],
                key="select_pev"
            )

            uploaded_file = st.file_uploader("Carregar Imagem", type=['png', 'jpg', 'jpeg'], key="file_uploader")
            
            if uploaded_file is not None and st.button("ENVIAR PROVA E ATUALIZAR STATUS"):
                st.success(f"Obrigado! Relatório para '{selected_pev}' enviado com sucesso. A coleta será agendada assim que possível.")
                
                st.session_state.report_flow = False 
                st.experimental_rerun()


    # --- ABA 2: Higiene Digital (Foco no Usuário) ---
    with tab2:
        st.header("🧠 Monitor de Bem-Estar Digital")
        st.markdown("""
        O uso consciente dos seus eletrônicos não é bom apenas para o planeta, mas para **sua saúde**. 
        O descarte de e-lixo é uma consequência do fim da vida útil dos aparelhos.
        """)
        
        st.subheader("Seu Desempenho")
        # Métricas de uso amigáveis 
        col_m1, col_m2, col_m3 = st.columns(3)
        
        col_m1.metric(
            label="Tempo de Tela (Média Diária)", 
            value="5h 30m", 
            delta="-30m vs. Semana Passada", 
            delta_color="inverse",
            help="Menos tempo de tela é melhor para a saúde dos olhos e para reduzir a necessidade de troca de aparelhos."
        )
        col_m2.metric(
            label="Alerta de Postura", 
            value="✅ OK", 
            delta="0 Alertas Hoje",
            help="Alerta automatizado que monitora sua postura ao usar o dispositivo."
        )
        col_m3.metric(
            label="Horas de Sono (Média)", 
            value="7h 15m", 
            delta="Melhora de 15m",
            help="Média de sono semanal. Dormir bem está diretamente ligado ao uso reduzido de eletrônicos antes de deitar."
        )
        
        # --- NOVO BLOCO: ANÁLISE DE ROTINA ---
        st.markdown("---")
        st.subheader("📝 Avalie sua Rotina Digital")
        st.write("Descreva brevemente como você utiliza seus dispositivos (horas de tela, uso antes de dormir, pausas, etc.) e receba uma avaliação instantânea dos seus hábitos.")

        # O formulário ajuda a manter a interface limpa após o clique do botão
        with st.form("routine_form"):
            routine_input = st.text_area(
                "Minha rotina digital:", 
                key="routine_input", 
                height=150,
                placeholder="Ex: Eu uso meu celular por cerca de 8 horas por dia. Olho o feed antes de dormir e acordo e já pego o aparelho."
            )
            
            # O botão de análise
            submitted = st.form_submit_button("Analisar Hábito Digital", type="secondary")

        if submitted:
            feedback = analyze_routine(routine_input)
            st.session_state['routine_feedback'] = feedback

        # Exibe o feedback se estiver disponível
        if 'routine_feedback' in st.session_state and st.session_state['routine_feedback']:
            st.markdown(f"#### Resultado da Análise:")
            # Usa os componentes de alerta do Streamlit para um feedback visual
            if 'Parabéns' in st.session_state['routine_feedback']:
                st.success(st.session_state['routine_feedback'])
            elif 'Atenção' in st.session_state['routine_feedback']:
                st.error(st.session_state['routine_feedback'])
            else:
                st.info(st.session_state['routine_feedback'])
        # --- FIM DO NOVO BLOCO ---

        st.markdown("---")
        st.subheader("💡 Dicas Rápidas: Uso Consciente e Descarte")
        st.write("""
        * **1. Priorize a Longevidade:** Evitar o uso excessivo e cuidar bem do seu aparelho é o primeiro passo para reduzir o e-lixo.
        * **2. Não Jogue no Lixo Comum:** Pilhas e eletrônicos possuem metais pesados que contaminam o solo e a água. Use sempre os PEVs.
        * **3. Faça Pausas:** Para cada hora de tela, descanse os olhos por 5 minutos para prevenir o cansaço visual.
        * **4. Apague seus Dados:** Sempre faça um reset de fábrica em celulares e computadores antes de descartar ou doar.
        """)


if __name__ == "__main__":
    app_principal()