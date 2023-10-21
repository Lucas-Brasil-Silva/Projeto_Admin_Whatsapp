# Importações das bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.chrome.options  import Options
from selenium.webdriver.support.ui    import WebDriverWait
from selenium.common.exceptions   import *
from selenium.webdriver.support  import expected_conditions as CondicaoEsperada
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By
from datetime import datetime
from time import sleep
import random

# Função para iniciar o driver do Selenium
def iniciar_driver():
    """
    Inicia um driver do Selenium e configura opções específicas.

    Retorna:
        driver: Uma instância do driver do Selenium.
        wait: Uma instância de WebDriverWait configurada.
    """

    chromeoptions = Options()
    arguments = ['--lang=pt-BR', 'window-size=900,750']
    for argument in arguments:
        chromeoptions.add_argument(argument)
    
    chromeoptions.add_experimental_option(
        'excludeSwitches', ['enable-logging'])

    chromeoptions.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(options=chromeoptions)

    # Configuração do WebDriverWait
    wait = WebDriverWait(
        driver,
        timeout=30,
        poll_frequency=1,
        ignored_exceptions=[
            ElementNotVisibleException,
            ElementNotInteractableException,
            NoSuchElementException,
        ]
        )

    return driver, wait

# Função para simular a digitação em um campo
def digitacao(texto, campo):
    """
    Simula a digitação de texto em um campo.

    Args:
        texto (str): O texto a ser digitado.
        campo: O elemento do campo onde o texto será digitado.
    """

    for letra in texto:
        campo.send_keys(letra)
        sleep(random.randint(2,5)/30)

# Função para introduzir pausas aleatórias
def pausas():
    """
    Introduz pausas aleatórias para simular o comportamento humano durante a automação.
    """
    
    sleep(random.randint(4,7)/1.8)
