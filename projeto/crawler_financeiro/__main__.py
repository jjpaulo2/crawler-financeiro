from . import json_downloader
from . import pdf_downloader

from .colors import ANSIColors

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