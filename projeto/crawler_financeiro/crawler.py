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
    HOSTNAME = 'https://www2.susep.gov.br'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 

    driver = webdriver.Chrome(options=options)
    driver.get(HOSTNAME + '/safe/menumercado/REP2/Produto.aspx/Consultar')

    search_box = driver.find_element_by_xpath('//input[@id="numeroProcesso"]')
    search_box.clear()
    search_box.send_keys(proccess['numeroprocesso'])
    search_box.send_keys(Keys.RETURN)

    sleep(2)
    download_button = driver.find_element_by_xpath('//a[@class="linkDownloadRelatorio"]')
    download_path = download_button.get_attribute('onclick')[15:-1]

    file_name = proccess['numeroprocesso'].replace('.', '-').replace('/', '-') + '.pdf'
    file_bytes = requests.get(HOSTNAME + download_path)
    with open('files/pdfs/' + file_name, 'wb') as file:
        file.write(file_bytes.content)

    driver.close()


def download_pdfs(proccess_list: list):
    """
    Função que itera a função `download_pdf` sobre uma lista de processos.

    Parameters:
        proccess_list (dict): lista de dicionários de processos já extraído do portal da SUSEP
    """
    i = 1
    quant_download = 5
    print(f"Baixando os primeiros {quant_download} arquivos de um total de {len(proccess_list)}.")

    for proccess in proccess_list:
        print('(%2d/%d) Baixando arquivo...' %(i, len(proccess_list)))
        download_pdf(proccess)
        i += 1
        
        if (i > quant_download): 
            break
    
    print("Download encerrado com sucesso.\n")

