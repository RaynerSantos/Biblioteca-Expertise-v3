import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import streamlit as st

LOGIN = "admin"
SENHA = 'Exp2025$'

# Caminho do arquivo JSON
# json_path = r"C:\PROJETOS\Biblioteca Expertise\biblioteca-expertise-4613ccbc3a7a.json"
json_path = "C:\PROJETOS\Biblioteca Expertise\biblioteca-expertise-4613ccbc3a7a.json"
# Definir escopo de acesso
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


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

df = buscar_biblioteca(json_path=json_path, scope=scope, worksheet='Livros')
print(f"\n{df}\n")


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


#=== 3º Passo - Inserção de livros ===#
def adicionar_livro(json_path, scope, LOGIN, TITULO, AUTOR):
    if LOGIN == 'admin' and SENHA == 'Exp2025$':
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


# # Alterar Status
# alterar_status_biblioteca(json_path=json_path, scope=scope, 
#                           LOGIN='rayner.santos', 
#                           SITUACAO='Disponível', # 'Emprestado' / 'Disponível'
#                           ID_LIVRO='1', 
#                           data=df)

# # Adicionar livro
# adicionar_livro(json_path=json_path, scope=scope, LOGIN=LOGIN, TITULO="O Hobbit", AUTOR="J.R.R. Tolkien")


