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


#=== 2º Passo - Alterar os status dos livros (Disponível, Emprestado, Não encontrado) ===#
def alterar_status_biblioteca(json_path, scope, LOGIN, SITUACAO, ID_LIVRO, data):
    if SITUACAO == 'Emprestado':
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'SITUACAO'] = 'Emprestado'
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'FUNCIONARIO'] = LOGIN
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'DATA_EMPRESTIMO'] = datetime.today().strftime("%Y-%m-%d")

        # # Autenticar no Google Sheets
        # credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        # client = gspread.authorize(credentials)

        # Carregar credenciais do Streamlit Secrets
        gcp_credentials = st.secrets["GCP_SERVICE_ACCOUNT"]

        # Converter a string JSON em um dicionário Python
        credentials_dict = json.loads(gcp_credentials)

        # Criar credenciais a partir do dicionário JSON
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(credentials)

        # Acessar a planilha
        spreadsheet = client.open("Controle_Livros_Expertise")  # Nome da planilha
        sheet = spreadsheet.worksheet("Livros")  # Nome da aba
        # Converter o DataFrame para uma lista de listas (formato aceito pelo gspread)
        data_atualizada = [data.columns.values.tolist()] + data.values.tolist()
        # Atualizar a planilha com os novos dados
        sheet.update(data_atualizada)
        print("\n✅ Planilha atualizada com sucesso!")

    elif SITUACAO == 'Disponível':
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'SITUACAO'] = 'Disponível'
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'FUNCIONARIO'] = 'NULL'
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'DATA_EMPRESTIMO'] = 'NULL'

        # # Autenticar no Google Sheets
        # credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        # client = gspread.authorize(credentials)

        # Carregar credenciais do Streamlit Secrets
        gcp_credentials = st.secrets["GCP_SERVICE_ACCOUNT"]

        # Converter a string JSON em um dicionário Python
        credentials_dict = json.loads(gcp_credentials)

        # Criar credenciais a partir do dicionário JSON
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = gspread.authorize(credentials)

        # Acessar a planilha
        spreadsheet = client.open("Controle_Livros_Expertise")  # Nome da planilha
        sheet = spreadsheet.worksheet("Livros")  # Nome da aba
        # Converter o DataFrame para uma lista de listas (formato aceito pelo gspread)
        data_atualizada = [data.columns.values.tolist()] + data.values.tolist()
        # Atualizar a planilha com os novos dados
        sheet.update(data_atualizada)
        print("\n✅ Planilha atualizada com sucesso!")

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

# Se o usuário não estiver autenticado, redireciona para a página inicial
if "login_sucesso" not in st.session_state or not st.session_state.login_sucesso:
    st.warning("❌ Você precisa fazer login!")
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
st.write("*Informe as opções desejadas abaixo para solicitar Empréstimo/Devolução do livro desejado.*")

#=== Criar formulário ===#
with st.form(key='alterar_status'):
    SITUACAO_USUARIO = st.selectbox('Selecione a opção desejada', options=['Empréstimo', 'Devolução'])
    ID_LIVRO = st.text_input(label="Insira o ID_LIVRO (Identificador do livro) desejado")
    input_buttom_submit = st.form_submit_button("Enviar")

# Criar um estado de sessão para verificar retorno da solicitação
if "retorno_solicitacao" not in st.session_state:
    st.session_state.retorno_solicitacao = False

# Se o botão for pressionado:
if input_buttom_submit:
    if ID_LIVRO not in dados['ID_LIVRO'].astype(str).values:
        st.warning("❌ ID_LIVRO não existe! Favor digitar um ID_LIVRO válido.")
    else:
        # Salvar os dados no session_state para a próxima página
        st.session_state.SITUACAO_USUARIO = SITUACAO_USUARIO
        st.session_state.ID_LIVRO = ID_LIVRO
        # Redireciona para a página Solicitacao.py
        st.switch_page("pages/Solicitacao.py")
