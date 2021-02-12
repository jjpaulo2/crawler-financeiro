FROM python:3.9-buster
LABEL author='João Paulo Carvalho <jjpaulo2@protonmail.com>'

#  Todos os comandos serão executados dentro do 
#  usuário root do container.

USER root

#  Faz download da última versão estável do Google Chrome
#  e instala as dependências do sistema:
#       - poppler-utils
#       - imagemagick
#       - tesseract-ocr
#       - tesseract-ocr-eng
# 
#  Também instala o Vim para fins de ajudar a ler o 
#  arquivo json final.

ARG CHROME_VERSION="google-chrome-stable"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -qqy \
    && apt-get -qqy install \
        ${CHROME_VERSION:-google-chrome-stable} \
        poppler-utils \
        imagemagick \
        tesseract-ocr \
        tesseract-ocr-eng \
        vim \
    && rm /etc/apt/sources.list.d/google-chrome.list \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

#  Faz download do ChromeDriver para poder utilizar
#  o Selenium Webdriver.

ARG CHROME_DRIVER_VERSION
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
    && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
    && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
    && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && rm -rf /opt/selenium/chromedriver \
    && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
    && rm /tmp/chromedriver_linux64.zip \
    && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
    && chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
    && ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver

#  Copia os arquivos do projeto para dentro do container
#  e instala as dependências.

COPY . /crawler
RUN cd /crawler \
    && python -m pip install -r requirements.txt

#  Script que será executado quando o container
#  for executando em modo interativo.

CMD cd /crawler \
    && python -m crawler_financeiro --help \
    && echo '' \
    && bash