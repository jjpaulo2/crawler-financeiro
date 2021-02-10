"""
Arquivo que contém as funções responsáveis pela extração do texto dos
arquivos PDFs.
"""
from PIL import Image
from pdf2image import convert_from_path
from time import sleep

import pytesseract
import os

def get_pdfs() -> list:
    '''
    Função que lê o diretório `files/pdfs` e retorna os arquivos
    já baixados.

    Returns:
        list: lista de todos os PDFs já armazenados localmente
    '''
    sleep(0.5)
    print('*     Obtendo lista de PDFs baixados.')
    files_names = os.listdir(r'files/pdfs')

    def filter_func(string: str) -> bool:
        # FILTRA APENAS ARQUIVOS TERMIDADOS COM .pdf
        return string.endswith('.pdf')

    files_names = list(filter(filter_func, files_names))

    sleep(0.5)
    print(f'      {len(files_names)} encontrado(s).')
    
    return files_names
    

def extract_pages(file_name: str) -> int:
    '''
    Função que extrai as páginas de um arquivo PDF para imagens
    no formato JPEG e as salva em `files/pdfs/tmp`.

    Params:
        file_name (str): nome do arquivo PDF que terá suas páginas extraídas

    Returns:
        int: número de páginas extraídas do arquivo
    '''
    file = f'files/pdfs/{file_name}'

    sleep(0.5)
    print('      Lendo as páginas...')
    # PREPARA O PDF PARA TER SUAS PÁGINAS SALVAS EM IMAGENS
    pages = convert_from_path(file, 200)
    
    page_counter = 1 # CONTADOR DE PÁGINAS

    for page in pages:
        # SALVA A PÁGINA COMO IMAGEM .jpg
        page_file = f'files/pdfs/tmp/page_{page_counter}.jpg'
        page.save(page_file, 'JPEG')

        page_counter += 1

    page_counter -= 1
    return page_counter

def get_pages_text(page_quantity: int, txt_file_output_name: str):
    '''
    Função que utiliza a biblioteca `Tesseract` para extrair o texto
    das imagens já salvas no diretório `files/pdfs/tmp`.

    Parameters:
        page_quantity (int): quantidade de páginas que serão lidas
        txt_file_output_name (str): nome do arquivo de texto que irá guardar o texto extraído
    '''
    sleep(0.5)
    print(f'      Extraindo texto para o arquivo "{txt_file_output_name}"')

    txt_file_output_path = f'files/pdfs/txt/{txt_file_output_name}'
    with open(txt_file_output_path, 'a') as output_txt:
        
        for i in range(1, page_quantity + 1):
            page_file = f'files/pdfs/tmp/page_{i}.jpg'
            
            # MÉTODO QUE EXTRAI O TEXTO DA IMAGEM
            text = pytesseract.image_to_string(Image.open(page_file))
            output_txt.write(text)

def clean_tmp_folder():
    '''
    Função que exclui todos os arquivos da pasta `files/pdfs/tmp`.
    '''
    sleep(0.5)
    print('*     Limpando arquivos temporários.')

    path = 'files/pdfs/tmp/'
    files = os.listdir(path)

    for file in files:
        os.remove(path + file)

def verify_file_exists(file_name: str) -> bool:
    '''
    Função que verifica se um arquivo já existe na pasta `files/pdfs`.

    Parameters:
        file_name (str): nome do arquivo que será verificado
    '''
    path = 'files/pdfs/txt/'
    exists = False

    try:
        with open(path + file_name, 'r'):
            exists = True
    
    finally:
        return exists


def proccess_pdf_folder():
    '''
    Função principal que executa todos as outras funções deste arquivo em ordem lógica.

    Algoritmo:
        1. Limpa os arquivos temporários
        2. Obtém a lista dos PDFs já salvos
        3. Itera a lista dos PDFs
        4. Verifica se o arquivo .txt correspondente já existe no sistema
            4.1. Se o arquivo não existir, então ele extrai as páginas e o texto delas
            4.2. Se o arquivo já existir, só passa para o próximo arquivo
    '''
    clean_tmp_folder()
    pdf_files = get_pdfs()

    counter = 1
    for file in pdf_files:
        print(f'({counter}/{len(pdf_files)}) Processando "{file}"')
        # REMOVE A EXTENSÃO `.pdf` E ADICIONA `.txt`
        txt_output_name = file[:-4] + '.txt'
        
        if not verify_file_exists(txt_output_name):
            pages = extract_pages(file)
            
            get_pages_text(pages, txt_output_name)
            clean_tmp_folder()
        
        else:
            sleep(0.5)
            print('*     Arquivo encontrado.')

        counter += 1

    sleep(0.5)
    print('*     Texto extraído com sucesso de todos os arquivos.\n')
