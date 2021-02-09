"""
Arquivo que contém os métodos responsáveis por fazer download 
dos arquivos JSON.
"""

import requests
import json

def download_starter_json() -> dict:
    """
    Função que faz o download do arquivo JSON inicial (sem filtros).
    O arquivo deverá ser salvo em `files/starter.json`.

    Returns:
        dict: dicionário com os dados obtidos no site da SUSEP.
    """
    url = "http://dados.susep.gov.br/olinda-ide/servico/produtos/versao/v1/odata/DadosProdutos?$format=json"
    
    print('(1/4) Fazendo o download...')
    req = requests.get(url, allow_redirects=True)

    print("(2/4) Formatando o arquivo...")
    json_formated = (req.content).decode('utf-8').replace("'", '"')
    json_final = json.loads(json_formated)
    json_output = json.dumps(json_final, indent=4)

    print('(3/4) Salvando o arquivo...')
    with open('files/starter.json', 'w') as file:
        file.write(json_output)

    print("(4/4) Arquivo salvo com sucesso.\n")
    return json_final

def filter_starter_json(starter_json: dict, tipoproduto_field: str) -> list:
    """
    Função que recebe o JSON sem filtro, e o valor do campo `tipoproduto`
    que será o filtro do JSON.

    Parameters:
        starter_json (dict): dicionário inicial sem nenhum filtro
        tipoproduto_field (str): valor do campo `tipoproduto` que será o filtro aplicado no `starter_json` 
    
    Returns:
        list: lista com os dicionários filtrados pelo campo `tipoproduto` informado
    """
    values = starter_json['value']
    
    def filter_func(json: dict):
        return json['tipoproduto'] == tipoproduto_field

    print('(1/4) Filtrando JSON...')
    print(f"      Filtro aplicado: tipoproduto == \"{tipoproduto_field}\"")
    filtered_json = list(filter(filter_func, values))

    print('(2/4) Formatando o arquivo filtrado...')
    filtered_json_output = json.dumps(filtered_json, indent=4)

    print('(3/4) Salvando o arquivo filtrado...')
    with open('files/filtered.json', 'w') as file:
        file.write(filtered_json_output)

    print('(4/4) Arquivo salvo com sucesso.\n')
    return filtered_json
