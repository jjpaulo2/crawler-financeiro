"""
Arquivo que será executado quando o módulo for chamado por linha de comando.
    python -m crawler_financeiro

O procedimento executado é:
    1. Faz o download dos JSONs com os dados iniciais. (`json_downloader.py`)
    2. Filtra os dados apenas para os valos interessados. (`json_downloader.py`)
    3. Utiliza os dados filtrados para fazer download dos PDFs com os regulamentos. (`pdf_downloader.py`)
    4. Extrai o texto dos PDFs baixados. (`pdf_reader.py`)
    5. Salva um JSON com os dados formatados da forma como é necessário ser lido. (`generate_final_json.py`)
"""
from . import json_downloader
from . import pdf_downloader
from . import pdf_reader
from . import generate_final_json

from .ansi_colors import ANSIColors

import argparse
import json

def main(proccess_quantity: int):
    '''
    Função que executa o procedimento padrão do módulo.

    Arguments:
        proccess_quantity (int): quantidade de processos que terão seus regulamentos baixados
    '''
    print('\n==================================')
    print('OBTENDO DADOS DO PORTAL DA SUSEP')
    print('==================================')
    print(f'Author: {ANSIColors.header("@jjpaulo2")}')
    print('-------------------\n')

    try:
        print(f"{ANSIColors.okgreen('#1.')}   OBTENDO JSON INICIAL")
        print('---')
        data = json_downloader.download_starter_json()

        print(f"{ANSIColors.okgreen('#2.')}   FILTRANDO DADOS")
        print('---')
        filtered_data = json_downloader.filter_starter_json(data, 'PLANO DE PREVIDÊNCIA')

        print(f"{ANSIColors.okgreen('#3.')}   BAIXANDO PDFS")
        print('---')
        downloaded_processes = pdf_downloader.download_pdfs(filtered_data, proccess_quantity)

        print(f"{ANSIColors.okgreen('#4.')}   EXTRAINDO TEXTO DOS PDFS")
        print('---')
        pdf_reader.proccess_pdf_folder()

        print(f"{ANSIColors.okgreen('#5.')}   GERANDO JSON FINAL COM OS DADOS EXTRAÍDOS")
        print('---')
        generate_final_json.generate_json_from_proccesses(downloaded_processes)

    except KeyboardInterrupt:
        print()
        print('==================================')
        print(' PROGRAMA ENCERRADO PELO USUÁRIO.')
        print('==================================')
        print()


# INICIALIZANDO O ARGPARSER PARA TRATAR ENTRADA DE LINHA DE COMANDO
description = f"""
==================================
 OBTENDO DADOS DO PORTAL DA SUSEP
==================================
 Author: {ANSIColors.header('@jjpaulo2')}
-------------------

Exemplo de uso:
    $ python -m crawler_financeiro --n 5

No caso do não uso do parêmetro [--n], a quantidade
padrão de processos será 3.
"""

parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawTextHelpFormatter
    )
parser.add_argument('--n', help='Número de processos que terão o seu PDF baixado.', type=int)

args = parser.parse_args()

if not args.n:
    proccess_quantity = 3

else:
    proccess_quantity = args.n

main(proccess_quantity)

