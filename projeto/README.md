## Módulo do crawler de dados financeiros

O módulo é capaz de realizar todas as tarefas pedidas no objetivo do desafio. Os dados que conseguí extrair do site e dos arquivos em PDF foram:

- `status do processo`
- `data de distribuição do regulamento`
- `taxa de juros`
- `taxa de carregamento`
- `período de carência`

### Execução via Docker

Existe um [`Dockerfile`](./Dockerfile) que monta um container com toda a configuração de ambiente necessária para rodar o módulo, e já vem munido do editor **Vim**. Para fazer a build, execute o seguinte comando.

```shell
$ docker build -t crawler_financeiro .
```

Para utilizar o módulo agora, basta executar:

```shell
$ docker run -it crawler_financeiro
```

Será exibida a mensagem de `help` do módulo e logo depois você entrará no `bash` do container. Agora, basta executar o módulo, conforme mostrado.

```shell
$ python -m crawler_financeiro
```

> Ao ser exibido o prompt `"Deseja visualizar o arquivo em um editor de texto? (s/n)"` insira "s" e depois 1 para abrir o **Vim**.

Para obter o arquivo `final_json.json` do container, basta sair do modo interativo e verificar o **id do container**. Depois, copiar o arquivo usando `docker cp`.

```shell
root@3f8851ddc2b3:/crawler# exit
exit

$ docker ps -a
{CONTAINER_ID}  crawler_financeiro  "/bin/sh -c 'cd /cra…" ...
...

$ docker cp {CONTAINER_ID}:/crawler/final_json.json .
```

### Execução manual

As dependências do projeto são geridas com **Pipenv**. Portanto, antes de tudo, garanta que tenha instalado.

```shell
$ pip install -U pipenv
```

Certifique-se de ter instalado o navegador **Google Chrome** ou **Chromium** e o **ChromeDriver** ([download aqui](https://chromedriver.chromium.org/downloads)) referente à sua versão do navegador no PATH do sistema.

Também será necessário instalar o **Poppler** para extrair as páginas dos arquivos PDF como imagens e a engine de OCR (Optical Character Recognition) **Tesseract** para extrair o texto destas imagens.

```shell
# INSTALAÇÃO NO DEBIAN/UBUNTU
$ sudo apt install poppler-utils imagemagick tesseract-ocr tesseract-ocr-eng

# INSTALAÇÃO NO ARCH/MANJARO
$ sudo pacman -S poppler tesseract tesseract-data-eng

# INSTALAÇÃO NO MAC OS
$ brew install poppler tesseract
```

Agora, com o **Pipenv**, **Poppler** e o **Tesseract** instalados na sua máquina, basta rodar os seguintes comandos.

```shell
$ pipenv install
$ pipenv shell
(projeto-P-F-DwQe) $
```

Agora você já está dentro do ambiente virtual do projeto, com todas as depedências instaladas e pronto para executar o módulo.

### Uso

O módulo é facilmente utilizável via linha de comando.

```shell
$ python -m crawler_financeiro --help

usage: crawler_financeiro [-h] [--n N]

==================================
 OBTENDO DADOS DO PORTAL DA SUSEP
==================================
 Author: @jjpaulo2
-------------------

Exemplo de uso:
    $ python -m crawler_financeiro --n 5

No caso do não uso do parêmetro [--n], a quantidade
padrão de processos será 3.

optional arguments:
  -h, --help  show this help message and exit
  --n N       Número de processos que terão o seu PDF baixado.
```

Você pode passar um parâmetro `--n` que indica o número de processos que irão ter suas informações extraídas. Por exemplo, no comando a baixo serão baixados os primeiros 8 documentos PDF do site da SUSEP.

```
$ python -m crawler_financeiro --n 8
```

O módulo irá exibir uma saída símilar à esta:

    ==================================
     OBTENDO DADOS DO PORTAL DA SUSEP
    ==================================
     Author: @jjpaulo2
    -------------------

    #1.   OBTENDO JSON INICIAL
    ---
    (1/4) Fazendo o download...
    (2/4) Formatando o arquivo...
    (3/4) Salvando o arquivo...
    (4/4) Arquivo salvo com sucesso.

    #2.   FILTRANDO DADOS
    ---
    (1/4) Filtrando JSON...
          Filtro aplicado: tipoproduto == "PLANO DE PREVIDÊNCIA"
    (2/4) Formatando o arquivo filtrado...
    (3/4) Salvando o arquivo filtrado...
    (4/4) Arquivo salvo com sucesso.

    #3.   BAIXANDO PDFS
    ---
    *     Baixando os primeiros 1 arquivos de um total de 6034.
    (1/1) Baixando arquivo...
          Obtendo o status do processo.
    *     Arquivo salvo com sucesso.
    *     Download encerrado com sucesso.

    #4.   EXTRAINDO TEXTO DOS PDFS
    ---
    *     Limpando arquivos temporários.
    *     Obtendo lista de PDFs baixados.
          1 encontrado(s).
    (1/1) Processando "15414-002558-2009-81.pdf"
          Lendo as páginas...
          Extraindo texto para o arquivo "15414-002558-2009-81.txt"
    *     Limpando arquivos temporários.
    *     Texto extraído com sucesso de todos os arquivos.

    #5.   GERANDO JSON FINAL COM OS DADOS EXTRAÍDOS
    ---
    (1/1) Gerando JSON final...
          Gerando dicionário de dados...
          Salvando arquivo JSON...
    *     JSON salvo com sucesso.

      ARQUIVO JSON SALVO COM SUCESSO.
      Arquivo: final_json.json

No final, será gerado um arquivo `final_json.json` na raiz do projeto. E o módulo irá exibir um prompt para saber se você deseja abrir o arquivo em algum editor de texto.

    Deseja visualizar o arquivo em um editor de texto? (s/n) s

    Abrir com:
    1) Vim
    2) Nano
    3) Emacs
    4) VS Code
    >> 

O arquivo aberto deverá ser parecido com este:

```json
[
    {
        "tipoproduto": "PLANO DE PREVID\u00caNCIA",
        "entnome": "ACVAT- PREVIDENCIA S.A.",
        "cnpj": "91167361000182",
        "numeroprocesso": "10.001828/00-21",
        "ramo": "PREV | PENS\u00c3O POR PRAZO CERTO INDIVIDUAL",
        "subramo": "N\u00c3O APLIC\u00c1VEL",
        "status": "Aprovado",
        "extracted": {
            "distribution_date": "08 de maic de 2000",
            "interest": "JUROS DE 1%",
            "charge_rate": "carregamento serd de 30%",
            "grace_period": "CARENCIA DE 12 {doze) MESES"
        }
    }
]
```

### Entendendo o funcionamento do módulo

O funcionamento do módulo segue os seguintes passos.

1. Através do módulo **requests**, é feita uma requisição para o endereço `http://dados.susep.gov.br/olinda-ide/servico/produtos/versao/v1/odata/DadosProdutos?$format=json` que retorna um **JSON** com uma série de dados sobre vários processos financeiros diferentes.
2. Depois, é feito um filtro `pure-python` que deixa apenas os itens em que o campo **tipoproduto** vale **"PLANO DE PREVIDÊNCIA"**.
3. Utilizando **Selenium Webdriver**, é feito um acesso ao endereço `https://www2.susep.gov.br/safe/menumercado/REP2/Produto.aspx/Consultar`, onde o formulário é preenchido com o número do processo já extraído do JSON do item `#2`. Então, é extraído o **status** do processo e o link de download do **regulamento**.
4. Com o link do regulamento em mãos, é feito o download dele com o auxílio do módulo **requests**.
5. O módulo **pdf2image** separa cada página dos arquivos PDFs em imagens `JPEG`.
6. Entra em ação agora, a engine **Tesseract** através do módulo **pytesseract**. Ela carrega as imagens das páginas e faz o reconhecimento do texto delas. Depois às armazena em um arquivo `.txt`.
7. Com a ajuda do módulo **re** do próprio Python, para expressões regulares, fazemos uma busca pelos dados que queremos no arquivo `.txt` salvo e os armazenamos em um `JSON` para cada processo.
8. Por fim, apenas juntamos cada `JSON` gerado em um único. Que resulta no arquivo `final_json.json`.

---
Made with :heart: by [@jjpaulo2](https://github.com/jjpaulo2)