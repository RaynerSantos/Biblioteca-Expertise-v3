# python -m streamlit run Login.py
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json
from datetime import datetime

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
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'FUNCIONARIO'] = ''
        data.loc[data['ID_LIVRO'].astype(int)==int(ID_LIVRO), 'DATA_EMPRESTIMO'] = ''

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
        nova_linha = [novo_n_livro, TITULO, AUTOR, "Disponível", "", ""]

        # Adicionar a nova linha no final da planilha
        sheet.append_row(nova_linha)

        print(f"\n✅ Livro '{TITULO}' de {AUTOR} adicionado com sucesso!")
    return

#=== 4º Passo - Inserção de Logins ===#
def adicionar_login(json_path, scope, LOGIN, LOGIN_incluir, SENHA_incluir, NOME_COMPLETO):
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
if ("SITUACAO_USUARIO" not in st.session_state or "ID_LIVRO" not in st.session_state) and ("TITULO" not in st.session_state or "AUTOR" not in st.session_state) and ("LOGIN_incluir" not in st.session_state):
    st.warning("❌ Nenhuma solicitação foi realizada! Volte à página anterior.")
    st.stop()

st.title("Retorno da solicitação")


if ("SITUACAO_USUARIO" in st.session_state and "ID_LIVRO" in st.session_state):
    if st.session_state.SITUACAO_USUARIO == 'Empréstimo' and st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'SITUACAO'] == 'Disponível':
        alterar_status_biblioteca(json_path=json_path, scope=scope, 
                            LOGIN=st.session_state.LOGIN, 
                            SITUACAO='Emprestado', 
                            ID_LIVRO=st.session_state.ID_LIVRO, 
                            data=st.session_state.dados)
        st.write(f"📌 Usuário: **{st.session_state.LOGIN}**")
        st.write(f"📌 ID do Livro selecionado: **{st.session_state.ID_LIVRO}**")
        st.write(f"📌 Título: **{st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'TITULO']}**")
        st.write(f"📌 Autor: **{st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'AUTOR']}**")
        st.write(f"📌 Ação: **{st.session_state.SITUACAO_USUARIO}**")

        st.write("")
        st.success("✅ Solicitação registrada com sucesso!")
        st.write("Você já pode pegar o livro na estante da Biblioteca Expertise")

    elif st.session_state.SITUACAO_USUARIO == 'Devolução':
        if st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'SITUACAO'] == 'Emprestado':
            if st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'FUNCIONARIO'].strip() == st.session_state.LOGIN.strip():
                alterar_status_biblioteca(json_path=json_path, scope=scope, 
                                        LOGIN=st.session_state.LOGIN, 
                                        SITUACAO='Disponível', 
                                        ID_LIVRO=st.session_state.ID_LIVRO, 
                                        data=st.session_state.dados)
                st.write(f"📌 Usuário: **{st.session_state.LOGIN}**")
                st.write(f"📌 ID do Livro selecionado: **{st.session_state.ID_LIVRO}**")
                st.write(f"📌 Título: **{st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'TITULO']}**")
                st.write(f"📌 Autor: **{st.session_state.dados.loc[int(st.session_state.ID_LIVRO)-1,'AUTOR']}**")
                st.write(f"📌 Ação: **{st.session_state.SITUACAO_USUARIO}**")

                st.write("")
                st.success("✅ Solicitação registrada com sucesso!")
                st.write("Favor devolver o livro na estante da Biblioteca Expertise")
            else:
                st.warning("❌ Você não pode devolver um livro que se encontra emprestado por outro login.")      
        else:
            st.warning("❌ Livro já se encontra disponível no momento. Não há necessidade de devolução.")
    else:
        st.warning("❌ Livro desejado não está disponível no momento.")


if st.session_state.SOLICITACAO_ADMIN_LIVRO:
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


if st.session_state.SOLICITACAO_ADMIN_ACESSOS:
    # Função para adicionar login
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