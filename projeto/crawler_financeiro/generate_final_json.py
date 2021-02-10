from time import sleep
from .ansi_colors import ANSIColors

import re, os
import json

def generate_proccess_dict(proccess_starter_data: dict, txt_file_name: str) -> dict:
    '''
    Função que gera o dicionário com os dados necessários e
    que será salvo como JSON.

    Parameters:
        proccess_starter_data (dict): dicionário inicial filtrado do processo
        txt_file_name (str): nome do arquivo de texto relacionado ao processo

    Returns:
        dict: dicionário contendo os dados extraídos do texto
    '''
    sleep(0.5)
    print('      Gerando dicionário de dados...')

    path = 'files/pdfs/txt/'
    with open(path + txt_file_name) as file:
        text = str(file.read())

        distribution_date = re.findall(r'[0-9]+ de .* de [0-9]*', text)
        distribution_date = distribution_date[0] if len(distribution_date) > 0 else ''

        interest = re.findall(r'juros.*[0-9]+%', text, flags=re.IGNORECASE)
        interest = interest[0] if len(interest) > 0 else ''

        charge_rate = re.findall(r'carregamento.*[0-9]+%', text, flags=re.IGNORECASE)
        charge_rate = charge_rate[0] if len(charge_rate) > 0 else ''

        grace_period = re.findall(r'car.ncia.*[0-9]+.*meses*', text, flags=re.IGNORECASE)
        grace_period = grace_period[0] if len(grace_period) > 0 else ''

        extracted_data = {'extracted': {
            'distribution_date': distribution_date,
            'interest': interest,
            'charge_rate': charge_rate,
            'grace_period': grace_period,
        }}

        proccess_final_data =  proccess_starter_data | extracted_data
        return proccess_final_data


def generate_proccess_json(proccess_final_data: dict, json_output_file_name: str):
    '''
    Função que gera o arquivo JSON a partir do dicionário.

    Parameters:
        proccess_final_data (dict): dicionário final do processo
        json_output_file_name (str): nome do arquivo JSON relacionado ao processo
    '''
    print('      Salvando arquivo JSON...')
    output_dict = json.dumps(proccess_final_data, indent=4)
    path = 'files/pdfs/json/'

    with open(path + json_output_file_name, 'w') as json_output:
        json_output.write(output_dict)
    
    print('*     JSON salvo com sucesso.')


def success_prompt():
    '''
    Função que exibe um prompt para abrir o arquivo 
    JSON salvo com um editor de texto.
    '''
    open_editor = input(' Deseja visualizar o arquivo em um editor de texto? (s/n) ')
    open_editor = open_editor.lower()

    if open_editor == 's':

        editors = ['vim', 'nano', 'emacs', 'code']
        print('\n Abrir com:')
        print(' 1) Vim')
        print(' 2) Nano')
        print(' 3) Emacs')
        print(' 4) VS Code')

        editor = int(input(ANSIColors.fail(' >> ')))
        os.system(editors[editor-1] + ' final_json.json')


def generate_json_from_proccesses(processes_list: list):
    '''
    Função que itera sobre uma lista de processos e gera os
    arquivos JSONs relacionados à cada uma delas.

    Parameters:
        processes_list (list): lista dos processos        
    '''
    complete_final_json = []
    process_counter = 1

    for proccess in processes_list:
        print(f'({process_counter}/{len(processes_list)}) Gerando JSON final...')

        file_name = proccess['numeroprocesso'].replace('/', '-').replace('.', '-')
        txt_file_name =  file_name + '.txt'
        json_file_name =  file_name + '.json'

        proccess_final_data = generate_proccess_dict(proccess, txt_file_name)
        complete_final_json.append(proccess_final_data)

        generate_proccess_json(proccess_final_data, json_file_name)

        process_counter += 1

    with open('final_json.json', 'w') as final_json:
        json_content = json.dumps(complete_final_json, indent=4)
        final_json.write(json_content)

    print(f'\n {ANSIColors.okcyan("ARQUIVO JSON SALVO COM SUCESSO.")}\n Arquivo: final_json.json')
    success_prompt()
