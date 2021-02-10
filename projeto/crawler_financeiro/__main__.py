"""
Arquivo que será executado quando o módulo for chamado por linha de comando.
    python -m crawler_financeiro

O procedimento executado é:
    1. Faz o download dos JSONs com os dados iniciais. (`json_downloader.py`)
    2. Filtra os dados apenas para os valos interessados. (`json_downloader.py`)
    3. Utiliza os dados filtrados para fazer download dos PDFs com os regulamentos. (`pdf_downloader.py`)
"""
from . import json_downloader
from . import pdf_downloader

from .ansi_colors import ANSIColors

print(f"""
==================================
 OBTENDO DADOS DO PORTAL DA SUSEP
==================================
 Author: {ANSIColors.header('@jjpaulo2')}
-------------------
""")

try:
    print(f"{ANSIColors.okgreen('#1.')}   OBTENDO JSON INICIAL")
    print('---')
    data = json_downloader.download_starter_json()

    print(f"{ANSIColors.okgreen('#2.')}   FILTRANDO DADOS")
    print('---')
    filtered_data = json_downloader.filter_starter_json(data, 'PLANO DE PREVIDÊNCIA')

    print(f"{ANSIColors.okgreen('#3.')}   BAIXANDO PDFS")
    print('---')
    pdf_downloader.download_pdfs(filtered_data)

except KeyboardInterrupt:
    print()
    print('==================================')
    print(' PROGRAMA ENCERRADO PELO USUÁRIO.')
    print('==================================')
    print()