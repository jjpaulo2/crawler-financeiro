from . import get_json, crawler

print("""
================================
OBTENDO DADOS DO PORTAL DA SUSEP
================================
Author: @jjpaulo2
-----------------
""")

try:
    print("#1.   OBTENDO JSON INICIAL")
    print('---')
    data = get_json.download_starter_json()

    print("#2.   FILTRANDO DADOS")
    print('---')
    filtered_data = get_json.filter_starter_json(data, 'PLANO DE PREVIDÊNCIA')

    print("#3.   BAIXANDO PDFS")
    print('---')
    crawler.download_pdfs(filtered_data)

except KeyboardInterrupt:
    print('\n')
    print('Programa encerrado pelo usuário.')
    print('')