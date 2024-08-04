# Projeto ETL com API do IBGE

Este projeto é um pipeline ETL (Extract, Transform, Load) que extrai dados de indicadores da API do IBGE, transforma esses dados em um formato adequado e os carrega em um banco de dados Oracle.

## Funcionalidades

- Extrai dados de indicadores da API do IBGE.
- Transforma os dados em DataFrames pandas.
- Realiza operações de limpeza e integração dos dados.
- Carrega os dados transformados em um banco de dados Oracle.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `pandas`
  - `requests`
  - `sqlalchemy`
  - `cx_Oracle`

## Configuração do Ambiente

### Ambiente Virtual (venv)

Este projeto foi feito utilizando um ambiente virtual (venv) para seu desenvolvimento. É recomendado criar um ambiente virtual para gerenciar as dependências do projeto.

python -m venv venv

```sh

etl_api
  - etl.ipynb        # Script inicial do pipeline ETL`
  - main.py          # Script principal do pipeline ETL`
  - senhabanco.txt   # Arquivo contendo a senha do banco de dados`
  - README.md        # Este arquivo README`


