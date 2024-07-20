import pandas as pd
import requests
import json

url = 'https://servicodados.ibge.gov.br/api/v1/paises/BR/indicadores/'
url_indicadores = 'https://servicodados.ibge.gov.br/api/v1/paises/indicadores/'

response = requests.get(url=url)
if response.status_code == 200:
    print(f'Sucesso na requisição - {response}')
else:
    print(f'Erro na requisição com o servidor - {response.status_code}')

dados_indicadores_json = response.json()
type(dados_indicadores_json)

