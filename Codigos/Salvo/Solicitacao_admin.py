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


#=== 3º Passo - Inserção de livros ===#
def adicionar_livro(json_path, scope, LOGIN, TITULO, AUTOR):
    if LOGIN == 'admin' and st.session_state.SENHA == 'Exp2025$':
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

        # Obter todas as linhas atuais para determinar o próximo ID_LIVRO
        data = sheet.get_all_values()

        # Definir o próximo número de livro automaticamente (incremento)
        if len(data) > 1:
            ultimo_numero = int(data[-1][0])  # Último ID_LIVRO (coluna 0)
            novo_n_livro = ultimo_numero + 1
        else:
            novo_n_livro = 1  # Se não houver livros, começa em 1

        # Criar a nova linha com os dados
        nova_linha = [novo_n_livro, TITULO, AUTOR, "NULL", "NULL", "Disponível"]

        # Adicionar a nova linha no final da planilha
        sheet.append_row(nova_linha)

        print(f"\n✅ Livro '{TITULO}' de {AUTOR} adicionado com sucesso!")
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
    adicionar_livro(json_path=json_path, scope=scope, 
                    LOGIN=st.session_state.LOGIN, 
                    TITULO=st.session_state.TITULO, 
                    AUTOR=st.session_state.AUTOR)
    
    st.write(f"📌 Usuário: **{st.session_state.LOGIN}**")
    st.write(f"📌 Título: **{st.session_state.TITULO}**")
    st.write(f"📌 Autor: **{st.session_state.AUTOR}**")
    st.write(f"📌 Ação: **Inserção de novo livro**")

    st.success("✅ Solicitação registrada com sucesso!")