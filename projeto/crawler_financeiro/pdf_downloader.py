"""
Arquivo que contém os métodos que baixam os pdf da página de download 
do regulamento, já com os JSONs dos números de processo baixados.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

import requests

# *
# Funções que realizam etapas do acesso ao site da SUSEP
# *

HOSTNAME = 'https://www2.susep.gov.br' # ENDEREÇO DO SITE DA SUSEP

def start_webdriver() -> webdriver.Chrome:
    '''
    Função que inicializa o Webdriver e acessa o site da SUSEP.

    Returns:
        webdriver.Chrome: objeto de webdriver do Chrome que pode ser utilizado
    '''
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # INICIALIZA O CHROME EM BACKGROUND

    sleep(0.5)
    # CARREGANDO SITE DE CONSULTA
    driver = webdriver.Chrome(options=options)
    driver.get(HOSTNAME + '/safe/menumercado/REP2/Produto.aspx/Consultar')
    
    return driver
    

def load_process_page(driver: webdriver.Chrome, process_number: str):
    '''
    Função que preenche o formulário com o número do processo.

    Parameters:
        driver (webdriver.Chrome): objeto de webdriver do Chrome
        process_number (str): número do processo a ser consultado
    '''
    sleep(0.5)
    search_box = driver.find_element_by_xpath('//input[@id="numeroProcesso"]')
    search_box.clear()
    search_box.send_keys(process_number)
    search_box.send_keys(Keys.RETURN)


def get_pdf_download_path(driver: webdriver.Chrome):
    '''
    Função que obtém o endereço de download do PDF de regulamento do processo.

    Parameters:
        driver (webdriver.Chrome): objeto de webdriver do Chrome
    '''
    sleep(0.5)
    download_button = driver.find_element_by_xpath('//a[@class="linkDownloadRelatorio"]')

    # RECORTA A STRING, DEIXANDO APENAS O CAMINHO PARA O ARQUIVO
    download_path = download_button.get_attribute('onclick')[15:-1]

    return download_path


def get_process_status(driver: webdriver.Chrome) -> str:
    '''
    Função que obtém o status do processo.

    Parameters:
        driver (webdriver.Chrome): objeto de webdriver do Chrome

    Returns:
        str: valor do status mostrado no site
    '''
    sleep(0.5)

    # OBTÉM A SITUAÇÃO DO PROCESSO
    situation = driver.find_element_by_xpath('//div[contains(.//strong, "Situação do Produto:")]')
    status = situation.text[20:]

    return status


# *
# Funções que fazem o processo completo
# *

def download_pdf(proccess: dict) -> dict:
    """
    Função que acessa a página de download do arquivo, preenche o 
    campo com o número do processo e faz o download do arquivo
    referente ao processo.

    Parameters:
        proccess (dict): dicionário de um único processo já extraído do portal da SUSEP

    Returns:
        dict: dicionário do processo atualizado com o campo de status do processo
    """
    process_number = proccess['numeroprocesso']
    file_name = process_number.replace('.', '-').replace('/', '-') + '.pdf'

    print('      Obtendo o status do processo.')
    driver = start_webdriver()
    load_process_page(driver, process_number)
    proccess['status'] = get_process_status(driver)

    try:
        # VERIFICA SE O ARQUIVO JÁ EXISTE.
        with open('files/pdfs/' + file_name, 'r') as file:
            driver.close()

            sleep(0.5)
            print('*     Arquivo encontrado.')

    except FileNotFoundError:
        # SE NÃO EXISTIR, BAIXA O DOCUMENTO E SALVA O ARQUIVO.

        download_path = get_pdf_download_path(driver)
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
    
    finally:
        return proccess


def download_pdfs(proccess_list: list, quant_download: int) -> list:
    """
    Função que itera a função `download_pdf` sobre uma lista de processos.

    Parameters:
        proccess_list (dict): lista de dicionários de processos já extraído do portal da SUSEP
        quant_download (int): quantidade de PDFs que serão baixados

    Returns:
        list: lista com os números dos processos baixados
    """
    i = 1 # CONTADOR DE PDFS BAIXADOS
    downloaded_proccess = [] # ARMAZENA O NÚMERO DOS PROCESSOS BAIXADOS
    print(f"*     Baixando os primeiros {quant_download} arquivos de um total de {len(proccess_list)}.")

    for proccess in proccess_list:
        print('(%d/%d) Baixando arquivo...' %(i, quant_download))

        tentativas = 0 # CONTADOR DE TENTATIVAS DE DOWNLOAD
        while tentativas < 3:
            # SERÃO FEITAS 3 TENTATIVAS DE BAIXAR O ARQUIVO.
            # SE NÃO FOREM BEM SUCEDIDAS, O DOWNLOAD PASSA PARA
            # O PRÓXIMO ARQUIVO.

            try:
                # BAIXA O PDF E RECEBE O NOVO DICT COM A SITUAÇÃO DO PROCESSO
                new_proccess = download_pdf(proccess)
                downloaded_proccess.append(new_proccess)
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

    return downloaded_proccess
