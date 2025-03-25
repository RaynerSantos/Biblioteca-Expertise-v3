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

# Se o usuário não estiver autenticado, redireciona para a página inicial
if "login_admin_sucesso" not in st.session_state or not st.session_state.login_admin_sucesso:
    st.warning("❌ Você precisa fazer login de administrador para entrar nessa página!")
    st.stop()

# Título da nova página
st.title("Biblioteca Expertise")
st.write("")  # Linha vazia
st.write(f"Bem-vindo, **{st.session_state.LOGIN}**! 😊")
st.write("")  # Linha vazia
st.write("📚 Lista de livros (Disponível / Emprestado)")

# Buscar dados da biblioteca
dados = buscar_biblioteca(json_path=json_path, scope=scope, worksheet='Livros')
st.session_state.dados = dados

# Exibir os dados
st.dataframe(dados, width=1500, height=500, hide_index=True)

st.write("")  # Linha vazia
st.write("*Informe abaixo o título e autor do livro que deseja incluir na Biblioteca Expertise*")

#=== Criar formulário ===#
with st.form(key='inserir_livros'):
    TITULO = st.text_input(label="Informe o nome do Título do livro que deseja incluir")
    AUTOR = st.text_input(label='Informe o nome do Autor do livro que deseja incluir')
    CATEGORIA = st.text_input(label='Informe a categoria do livro')
    SINOPSE = st.text_input(label='Informe a sinopse do livro')
    input_buttom_submit = st.form_submit_button("Enviar")
    st.session_state.TITULO = TITULO
    st.session_state.AUTOR = AUTOR
    st.session_state.CATEGORIA = CATEGORIA
    st.session_state.SINOPSE = SINOPSE

# Se o botão for pressionado:
if input_buttom_submit:
    st.session_state.SOLICITACAO_ADMIN_LIVRO = True # Define o estado do solicitacao do administrador como verdadeiro
    # Redireciona para a página Solicitacao_admin.py 
    st.switch_page("pages/Solicitacao.py")



# Linha divisória horizontal
# st.markdown("<hr>", unsafe_allow_html=True)
st.write("")
st.write("")
st.write("📑 Lista de Logins e senhas")

# Buscar dados da biblioteca
acessos = buscar_biblioteca(json_path=json_path, scope=scope, worksheet='Logins')
st.session_state.acessos = acessos

# Exibir os dados
st.dataframe(acessos, width=1500, height=500, hide_index=True)

st.write("")  # Linha vazia
st.write("*Informe abaixo o título e autor do livro que deseja incluir na Biblioteca Expertise*")

#=== Criar formulário ===#
with st.form(key='inserir_logins'):
    LOGIN_incluir = st.text_input(label="Informe o LOGIN que deseja incluir")
    SENHA_incluir = st.text_input(label='Informe a nova SENHA que deseja incluir para o login acima')
    NOME_COMPLETO = st.text_input(label='Informe o nome completo do novo usuário')
    input_buttom_submit_acessos = st.form_submit_button("Enviar")
    st.session_state.LOGIN_incluir = LOGIN_incluir
    st.session_state.SENHA_incluir = SENHA_incluir
    st.session_state.NOME_COMPLETO = NOME_COMPLETO

# Se o botão for pressionado:
if input_buttom_submit_acessos:
    st.session_state.SOLICITACAO_ADMIN_ACESSOS = True # Define o estado do solicitacao do administrador como verdadeiro
    if st.session_state.TITULO == "":
        st.session_state.SOLICITACAO_ADMIN_LIVRO = False
    # Redireciona para a página Solicitacao_admin.py
    st.switch_page("pages/Solicitacao.py")