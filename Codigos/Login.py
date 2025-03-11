# python -m streamlit run Login.py
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json
from datetime import datetime
# from Funcoes_Biblioteca import buscar_biblioteca, alterar_status_biblioteca, adicionar_livro

#=== 1º Passo - Função para buscar a tabela desejada no google sheets ===#
def buscar_biblioteca(json_path, scope, worksheet):
    # # Autenticar no Google Sheets usando a chave JSON
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
    spreadsheet = client.open("Controle_Livros_Expertise")
    sheet = spreadsheet.worksheet(worksheet)

    # Obter todos os valores da planilha
    data = sheet.get_all_values()

    # Converter para um DataFrame do Pandas
    data = pd.DataFrame(data[1:], columns=data[0])  # A primeira linha vira cabeçalho
    # data["ID_LIVRO"] = data["ID_LIVRO"].astype(int)
    return data

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

# # Configurações da página
# st.set_page_config(layout="centered")  # "wide" / "centered"

#=== Título ===#
st.title("Biblioteca Expertise")

# Criar um estado de sessão para verificar login
if "login_sucesso" not in st.session_state:
    st.session_state.login_sucesso = False

# Criar um estado de sessão para verificar login de administrador
if "login_admin_sucesso" not in st.session_state:
    st.session_state.login_admin_sucesso = False

# Formulário de login
with st.form(key="login"):
    LOGIN = st.text_input(label="Insira o seu login de acesso")
    SENHA = st.text_input(label="Insira a sua senha", type='password')
    input_buttom_submit = st.form_submit_button("Entrar")

# Se o botão for pressionado, verifica login
if input_buttom_submit:
    df_logins = buscar_biblioteca(json_path=json_path, scope=scope, worksheet='Logins')
    if ((df_logins['LOGIN'] == LOGIN) & (df_logins['SENHA'] == SENHA)).any():
        st.session_state.login_sucesso = True  # Define o estado do login como verdadeiro
        st.session_state.LOGIN = LOGIN  # Salva o usuário na sessão
        st.session_state.SENHA = SENHA # Salva a senha do usuário na sessão
        if LOGIN == 'admin':
            st.session_state.login_admin_sucesso = True
        st.rerun()  # Recarrega a página para aplicar a mudança
    else:
        st.warning("❌ Login ou senha incorretos!")

# Se login for bem-sucedido, redireciona para a página de livros e ou página do Administrador
if st.session_state.login_sucesso and LOGIN == 'admin':
    st.switch_page("pages/Administrador.py")

elif st.session_state.login_sucesso:
    st.switch_page("pages/Livros.py")