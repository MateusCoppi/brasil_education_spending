import pandas as pd
import requests
import json
from sqlalchemy import create_engine, DECIMAL, Column, Integer, String
import cx_Oracle

# URLs da API
URL_BASE_IBGE = 'https://servicodados.ibge.gov.br/api/v1/paises/'
URL_INDICADORES = URL_BASE_IBGE + 'indicadores/'

# Caminho para as credenciais do banco de dados
PATH_CRED_BANCO = 'D:\\Projetos\\etl_api\\senhabanco.txt'

response = requests.get(url=URL_BASE_IBGE)
if response.status_code == 200:
    print(f'Sucesso na requisição - {response}')
else:
    print(f'Erro na requisição com o servidor - {response.status_code}')

dados_indicadores_json = response.json()

def get_api_ibge(pais: str, indicador: int):
    url = f'https://servicodados.ibge.gov.br/api/v1/paises/{pais}/indicadores/{indicador}'
    response = requests.get(url=url)
    if response.status_code == 200:
        print(f'Sucesso na requisição - {response}')
    else:
        print(f'Erro na requisição com o servidor - {response.status_code}')

    json_data = response.json()
    return json_data


dados_gastos_educacao = get_api_ibge('BR', 77819)
dict_gastos_educacao = dados_gastos_educacao[0]
df = pd.DataFrame(dados_gastos_educacao[0]['series'][0]['serie'][1:])
df = pd.melt(df, var_name='Ano', value_name='Valor').dropna().reset_index()
df = df[['Ano', 'Valor']]
print('\n****DataFrame Dados de Educação Criado com Sucesso****')

df['id_unidade'] = dict_gastos_educacao['unidade']['id']
df['id_pais'] = dict_gastos_educacao['series'][0]['pais']['id']
df['multiplicador'] = dict_gastos_educacao['unidade']['multiplicador']
df_dados_educacao = df[['id_pais', 'id_unidade', 'multiplicador', 'Ano', 'Valor']]
df_dados_educacao['Valor'] = pd.to_numeric(df_dados_educacao['Valor'], errors='coerce').astype(float)
print('****DataFrame Dados de Educação Tratado com Sucesso****')

pib = get_api_ibge('BR', 77827)
df_pib = pd.DataFrame(pib[0]['series'][0]['serie'][1:])
df_pib = pd.melt(df_pib, value_name='Valor_PIB', var_name='Ano').dropna()
print('\n****DataFrame Dados do PIB Criado com Sucesso****')

df_pib = df_pib[['Ano', 'Valor_PIB']]
df_pib['Valor_PIB'] = pd.to_numeric(df_pib['Valor_PIB'], errors='coerce').astype(float)

df_tratado = pd.merge(df_dados_educacao, df_pib, on='Ano', how='inner')
df_tratado['Ano'] = df_tratado['Ano'].astype((int))
df_tratado['gasto_educacao'] = ( df_tratado['Valor'] * df_tratado['Valor_PIB'] ) / 100
df_tratado = df_tratado[['id_pais', 'multiplicador', 'Ano', 'Valor', 'Valor_PIB', 'gasto_educacao']]
df_tratado.columns = ['id_pais', 'multiplicador', 'ano', 'gasto % pib', 'valor_pib_ano', 'gasto_educacao_ano']
print('****DataFrame Dados do PIB Tratado com Sucesso****')

with open(PATH_CRED_BANCO, 'r') as file:
    pass_banco = file.read()

engine = create_engine(f"oracle://projetos:{pass_banco}@localhost:1521/?service_name=XEPDB1")
tipo_dados = {
    'id_pais': String(10),
    'multiplicador': Integer,
    'ano': Integer,
    'gasto % pib': DECIMAL(30,2),
    'valor_pib_ano': DECIMAL(30,2),
    'gasto_educacao_ano': DECIMAL(30,2)
}
df_tratado.to_sql('gastos_educacao', con=engine, if_exists='replace', index=False, dtype=tipo_dados)
print('\n****Dados Inseridos no Banco de Dados****')