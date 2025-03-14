# python -m streamlit run Login.py
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json
from datetime import datetime
# from Funcoes_Biblioteca import buscar_biblioteca, alterar_status_biblioteca, adicionar_livro

#=== 3º Passo - Inserção de Logins ===#
def adicionar_login(json_path, scope, LOGIN, LOGIN_incluir, SENHA_incluir, NOME_COMPLETO):
    if LOGIN == 'admin' and st.session_state.SENHA == 'Exp2025$':
        # # Autenticar no Google Sheets
        # credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        # client = gspread.authorize(credentials)

        # Carregar credenciais do Streamlit Secrets
        gcp_credentials = st.secrets["GCP_SERVICE_ACCOUNT"]

        # Converter a string JSON em um dicionário Python
        credentials_dict = json.loads(gcp_credentials)

        # Criar credenciais a partir do dicionário JSON e Autenticar no Google Sheets
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(credentials)

        # Acessar a planilha
        spreadsheet = client.open("Controle_Livros_Expertise")  # Nome da planilha
        sheet = spreadsheet.worksheet("Logins")  # Nome da aba

        # Criar a nova linha com os dados
        nova_linha = [LOGIN_incluir, SENHA_incluir, NOME_COMPLETO]

        # Adicionar a nova linha no final da planilha
        sheet.append_row(nova_linha)

        print(f"\n✅ Login '{LOGIN_incluir}' adicionado com sucesso!")
    return

# CSS personalizado
st.markdown(
    """
    <style>
    /* Cor de fundo da página */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
    }
    
    /* Cor de fundo do cabeçalho */
    [data-testid="stHeader"] {
        background-color: #000000;
    }

    /* Cor de fundo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #333333;
    }

    /* Cor do título */
    h1 {
        color: #FFFFFF; /* Laranja avermelhado */
        text-align: center;
    }

    /* Cor do subtítulo */
    h2 {
        color: #FFD700; /* Dourado */
    }

    /* Cor do texto normal */
    p, span {
        color: #FFFFFF; /* Branco */
    }

    /* Cor dos botões */
    button {
        background-color: #20541B !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Caminho do arquivo JSON
# json_path = r"C:\PROJETOS\Biblioteca Expertise\biblioteca-expertise-4613ccbc3a7a.json"
json_path = "C:\PROJETOS\Biblioteca Expertise\biblioteca-expertise-4613ccbc3a7a.json"
# Definir escopo de acesso
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Verifica se o usuário chegou corretamente na página
if "solicitacao_admin" not in st.session_state:
    st.warning("❌ Nenhuma solicitação foi realizada! Volte à página anterior.")
    st.stop()

st.title("Retorno da solicitação")

if st.session_state.solicitacao_admin:
    # Função para adicionar livro
    adicionar_login(json_path=json_path, scope=scope, 
                    LOGIN=st.session_state.LOGIN,
                    LOGIN_incluir=st.session_state.LOGIN_incluir, 
                    SENHA_incluir=st.session_state.SENHA_incluir, 
                    NOME_COMPLETO=st.session_state.NOME_COMPLETO)
    
    st.write(f"📌 Usuário: **{st.session_state.LOGIN}**")
    st.write(f"📌 Login adicionado: **{st.session_state.LOGIN_incluir}**")
    st.write(f"📌 Senha: **{st.session_state.SENHA_incluir}**")
    st.write(f"📌 Ação: **Inserção de novo usuário**")

    st.success("✅ Solicitação registrada com sucesso!")