import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# ID da planilha (extraído do link)
sheet_id  = "1R6eatYbbOSAFsWzxAA-fTh5la8IMrnQJ"

# Nome da aba (verifique no Google Sheets)
sheet_name = "Livros"

# Construir a URL de exportação no formato CSV
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Ler os dados diretamente do Google Sheets
df = pd.read_csv(url)

# Exibir o DataFrame
print(df)