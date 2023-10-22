"""
O programa requer a biblioteca Selenium para automatizar as interações com o WhatsApp Web e é projetado para ser executado em segundo plano enquanto o navegador está aberto. 

Certifique-se de que as bibliotecas necessárias estejam instaladas e configuradas corretamente no seu ambiente de execução. 

Certifique-se também de que você tenha instalado o WebDriver apropriado para o navegador que deseja automatizar.
"""

# Importação de bibliotecas
from driver import iniciar_driver, digitacao, pausas, CondicaoEsperada, By # Importa funções personalizadas
from os import linesep
import keyboard
import pyautogui
from time import sleep
import csv

def respondendo_membro(driver,wait):
    """ 
    Essa função é responsável por verificar as mensagens recebidas e responder a saudações específicas. Ela extrai informações sobre as mensagens, verifica se há mensagens de saudação não respondidas e, se necessário, responde a elas. As respostas são registradas em um arquivo CSV chamado 'saudacoes-dia.csv'. 
    """

    saudacoes = ['Bom dia','bom dia','Boa tarde','boa tarde','Boa noite','boa noite']

    try:
        dados = wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@role="row"]//div[@data-pre-plain-text]')))

        data_mensagem = [[dado.get_attribute('data-pre-plain-text').split(' ')[1].replace(']',''),dado.get_attribute('data-pre-plain-text').split(' ')[2].replace(':','') if not dado.get_attribute('data-pre-plain-text').split(' ')[2].replace('+','').isdigit() else ' '.join(dado.get_attribute('data-pre-plain-text').split(' ')[2:5]).replace(':','')] for dado in dados]
        
        mensagens_hj = [[id,dado[1]] for id, dado in enumerate(data_mensagem) if datetime.now().strftime('%d/%m/%Y') == dado[0]]

        mensagens = [[mens[1],dados[mens[0]].text] for mens in mensagens_hj if mens[1] != 'Lucas' and dados[mens[0]].text in saudacoes]
    except Exception as erro:
        print(erro)
        mensagens = []

    try:
        with open('saudacoes-dia.csv','r',encoding='UTF-8') as arquivo:
            arquivo_ = csv.reader(arquivo)
            respostas = [linha for linha in arquivo_]
    except FileNotFoundError:
        respostas = []

    hoje = datetime.now().strftime('%d/%m/%Y')
    for men in mensagens:
        frase = [frase for nome,frase,dia in respostas if nome == men[0] and dia == hoje]

        if not all(hoje in dia for nome,frase,dia in respostas):
            with open('saudacoes-dia.csv','w',encoding='UTF-8') as arquivo:
                arquivo.write('')

        if not men[1] in frase:
            campo_mensagem = wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"]')))
            marcar = f'@{men[0]}'
            digitacao(texto=marcar,campo=campo_mensagem)
            pausas()
            campo_mensagem.send_keys(Keys.TAB)
            digitacao(texto=men[1],campo=campo_mensagem)
            pausas()
            campo_mensagem.send_keys(Keys.ENTER)
            pausas()

            with open('saudacoes-dia.csv','a',encoding='UTF-8') as arquivo:
                arquivo.write(f'{men[0]},{men[1]},{hoje}\n')

def remover_membro(driver, wait):
    """
    Essa função remove membros de grupos e apaga mensagens. Ela obtém informações sobre os membros do grupo e os links para seus perfis, depois clica em "Remover" para expulsar os membros do grupo. Além disso, essa função também apaga mensagens.
    """

    try:
        dados = [element.text for element in wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]/div[@role="row"]//div[@class="_1BOF7 _2AOIt"]')))]
        pausas()

        membros = set([dado.split('\n')[0] for dado in dados if 'https:' in dado])
        links = [id for id,dado in enumerate(dados) if 'https:' in dado]
    except Exception as erro:
        print(erro)
        membros, links = [], []

    for id in links:
        try:
            dados = [element.text for element in wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]/div[@role="row"]//div[@class="_1BOF7 _2AOIt"]')))]
            pausas()

            link = [id for id,dado in enumerate(dados) if 'https:' in dado]

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//span[@class="kiiy14zj"]'))).click()
            pausas()

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="Selecionar mensagens"]'))).click()
            pausas()
        
            wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="g0rxnol2 l7jjieqr dh5rsm73 hpdpob1j neme6l2y ajgl1lbb dntxsmpk ixn6u0rb s2vc4xk1 o0wkt7aw cgi16xlc"]')))[link[0]].click()
            pausas()

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//span[@data-icon="delete"]'))).click()
            pausas()

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="Apagar para todos"]'))).click()
            pausas()

            try:
                wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="Apagar para todos"]'))).click()
                pausas()
            except Exception as erro:
                print(erro)

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="OK"]'))).click()
            pausas()
        except Exception as erro:
            print(erro)
        
        try:
            dados = [element.text for element in wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]/div[@role="row"]//div[@class="_1BOF7 _2AOIt"]')))]

            apagar_mensagem = [id for id,dado in enumerate(dados) if 'Mensagem apagada por um admin' in dado]

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//span[@class="kiiy14zj"]'))).click()
            pausas()

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="Selecionar mensagens"]'))).click()
            pausas()
        
            for apagar in apagar_mensagem:
                wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="g0rxnol2 l7jjieqr dh5rsm73 hpdpob1j neme6l2y ajgl1lbb dntxsmpk ixn6u0rb s2vc4xk1 o0wkt7aw cgi16xlc"]')))[apagar].click()
                pausas()

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//span[@data-icon="delete"]'))).click()
            pausas()

            wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="Apagar para mim"]'))).click()
            pausas()
        except Exception as erro:
            print(erro)

    for nome in membros:
        wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[@class="_2au8k"]'))).click()
        pausas()

        wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[@class="kk3akd72 a3oefunm"]/span[@data-icon="search"]'))).click()
        pausas()

        campo_nome = wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//p[@class="selectable-text copyable-text iq0m558w g0rxnol2"]')))
        digitacao(nome,campo_nome[0])
        pausas()

        wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="_8nE1Y"]/div[@role="gridcell"]')))[0].click()
        pausas()

        wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[text()="Remover"]'))).click()
        pausas()
        
        campo_nome[0].send_keys(Keys.ESCAPE)
        pausas()
        wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[@class="kk3akd72 p6y6hbba"]/div[@role]'))).click()
        pausas()

def saudando_novo_membro(driver,wait):
    """
    Esta função verifica se há novos membros no grupo e os saúda. Ela verifica as entradas de membros recém-chegados e, se houver algum membro novo, envia uma saudação para eles. Os membros recém-chegados são registrados em um arquivo chamado 'membros.txt'.
    """

    try:
        entrada = [element.text for element in wait.until(CondicaoEsperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="_2OvAm focusable-list-item _1jHIY"]//div[@class="_1sykI"]')))]
        pausas()

        novo_membro = set([frase.split('\n')[0] for frase in entrada if 'entrou usando um link de convite' in frase.split('\n')[1:]])
    except Exception as erro:
        print(erro)
        novo_membro = []

    try:
        with open('membros.txt','r',encoding='UTF-8') as arquivo:
            membros = arquivo.read().split('\n')
    except FileNotFoundError:
        membros = ''

    for membro in novo_membro:
        if not membro in membros:
            campo_mensagem = wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"]')))
            digitacao(texto='@'+membro,campo=campo_mensagem)
            pausas()
            campo_mensagem.send_keys(Keys.TAB)
            frase = 'Seja Bem vindo ao grupo!!'
            digitacao(texto=frase,campo=campo_mensagem)
            pausas()
            campo_mensagem.send_keys(Keys.ENTER)
            pausas()

            with open('membros.txt','a',encoding='UTF-8') as arquivo:
                arquivo.write(f'{membro}\n')

def main():
    """
    A função principal do programa, que inicializa o driver do Selenium, abre o WhatsApp Web no navegador, insere um número de telefone e aguarda a autenticação. Depois, ele entra no grupo especificado e inicia um loop que chama as outras funções para responder a mensagens, remover membros e saudar novos membros. O programa continua em execução até que a tecla de espaço seja pressionada.
    """

    driver, wait = iniciar_driver()

    driver.get('https://web.whatsapp.com/')
    sleep(5)

    numero = pyautogui.prompt(text='Digite seu número:',title='Numero')
    grupo = pyautogui.prompt(text='Digite o nome do Grupo:',title='Grupo')
 
    driver.execute_script('window.scrollTo(0,200);')
    pausas()
    wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//span[@role="button"]'))).click()

    campo_numero = wait.until(CondicaoEsperada.visibility_of_element_located((By.XPATH , '//form/input[@aria-label="Insira seu número de telefone."]')))
    pausas()
    digitacao(numero,campo_numero)

    wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, '//div[@role="button"]/div'))).click()

    codigo = wait.until(CondicaoEsperada.visibility_of_element_located((By.XPATH, '//div[@class="tvf2evcx m0h2a7mj lb5m6g5c j7l1k36l ktfrpxia nu7pwgvd p357zi0d dnb887gk gjuq5ydh i2cterl7 ac2vgrno sap93d0t gndfcl4n light"]'))).text.replace('\n','')

    texto = f'Use o código a seguir para abrir o WhatsApp Web no Chrome através do seu celular.{linesep}🔑🔑 Código: {codigo}{linesep}Não continue sem fazer a liberação Conectando um aparelho'
    pyautogui.alert(text=texto,title='Whatsapp Web',button='Continuar')
    aviso = f'Aguarde até que o WhatsApp abrir no seu navegador, para que não ocorrera erros.{linesep}Após isso pode clicar em continuar!!'
    pyautogui.alert(text=aviso,title='Aviso',button='Continuar')

    grupo = 'Grupo'
    wait.until(CondicaoEsperada.element_to_be_clickable((By.XPATH, f'//div[@class="_21S-L"]//span[text()="{grupo}"]'))).click()
    pausas()

    while keyboard.is_pressed('space') == False:
    
        respondendo_membro(driver,wait)

        remover_membro(driver,wait)

        saudando_novo_membro(driver,wait)
    
    driver.close()

if __name__ == '__main__':
    main()