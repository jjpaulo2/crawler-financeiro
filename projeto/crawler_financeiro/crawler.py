"""
Arquivo que contém os métodos que baixam os pdf da página de download 
do regulamento, já com os JSONs dos números de processo baixados.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

import requests

def download_pdf(proccess: dict):
    """
    Função que acessa a página de download do arquivo, preenche o 
    campo com o número do processo e faz o download do arquivo
    referente ao processo.

    Parameters:
        proccess (dict): dicionário de um único processo já extraído do portal da SUSEP
    """
    file_name = proccess['numeroprocesso'].replace('.', '-').replace('/', '-') + '.pdf'
    
    try:
        # VERIFICA SE O ARQUIVO JÁ EXISTE.
        with open('files/pdfs/' + file_name, 'r') as file:
            sleep(0.5)
            print('*     Arquivo encontrado.')

    except FileNotFoundError:
        # SE NÃO EXISTIR, BAIXA O DOCUMENTO E SALVA O ARQUIVO.

        HOSTNAME = 'https://www2.susep.gov.br'

        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # INICIALIZA O CHROME EM BACKGROUND

        driver = webdriver.Chrome(options=options)
        driver.get(HOSTNAME + '/safe/menumercado/REP2/Produto.aspx/Consultar')

        search_box = driver.find_element_by_xpath('//input[@id="numeroProcesso"]')
        search_box.clear()
        search_box.send_keys(proccess['numeroprocesso'])
        search_box.send_keys(Keys.RETURN)

        sleep(1)
        download_button = driver.find_element_by_xpath('//a[@class="linkDownloadRelatorio"]')
        # RECORTA A STRING, DEIXANDO APENAS O CAMINHO PARA O ARQUIVO
        download_path = download_button.get_attribute('onclick')[15:-1]
        
        driver.close()

        file_bytes = requests.get(HOSTNAME + download_path)

        if file_bytes.ok: 
            # SE O DOWNLOAD OCORRER DE FORMA CORRETA, O ARQUIVO SERÁ SALVO
            with open('files/pdfs/' + file_name, 'wb') as file:
                file.write(file_bytes.content)
                print("*     Arquivo salvo com sucesso.")
        
        else:
            # SENÃO, SERÁ LANÇADA UMA EXCEÇÃO DE CONEXÃO
            raise ConnectionError


def download_pdfs(proccess_list: list):
    """
    Função que itera a função `download_pdf` sobre uma lista de processos.

    Parameters:
        proccess_list (dict): lista de dicionários de processos já extraído do portal da SUSEP
    """
    i = 1 # CONTADOR DE PDFS BAIXADOS
    quant_download = 5 # LIMITA A QUANTIDADE DE PDFS BAIXADOS
    print(f"*     Baixando os primeiros {quant_download} arquivos de um total de {len(proccess_list)}.")

    for proccess in proccess_list:
        print('(%d/%d) Baixando arquivo...' %(i, quant_download))

        tentativas = 0 # CONTADOR DE TENTATIVAS DE DOWNLOAD
        while tentativas < 3:
            # SERÃO FEITAS 3 TENTATIVAS DE BAIXAR O ARQUIVO.
            # SE NÃO FOREM BEM SUCEDIDAS, O DOWNLOAD PASSA PARA
            # O PRÓXIMO ARQUIVO.

            try:
                download_pdf(proccess)
                break

            except Exception:
                # SE OCORRER ERRO NO DOWNLOAD, SERÁ EXIBIDA UMA MENSAGEM DE ERRO
                # E A QUANTIDADE DE TENTATIVAS SERÁ INCREMENTADA.
                print('*     Erro inesperado ao tentar baixar o arquivo. Tentando novamente.')
                tentativas += 1

        else:
            # QUANDO OCORREREM 3 TENTATIVAS, O LOOP SERÁ ENCERRADO E ESTA MENSAGEM SERÁ EXIBIDA.
            print('*     Máximo de tentativas alcançado. Baixando próximo arquivo.')

        i += 1
        if (i > quant_download): 
            break
    
    sleep(0.5)
    print("*     Download encerrado com sucesso.\n")
