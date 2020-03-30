from selenium import webdriver
from twilio.rest import Client
import time
from datetime import datetime
#from datetime import date

def envia_sms(preco):
    account_sid = 'SID DA PLATAFORMA TWILIO'
    auth_token = 'AUTH TOKEN DA PLATAFORMA TWILIO'
    client = Client(account_sid, auth_token)

    message = client.messages \
            .create(
                 body= f'O preco do produto esta R$ {preco}',
                 from_='+NÚMERO DA PLATAFORMA TWILIO',
                 to='NÚMERO QUE VAI RECEBER O SMS'
             )

url = 'https://www.amazon.com.br/gp/product/B07L59CTYJ/ref=ox_sc_act_title_1?smid=A1ZZFT5FULY4LN&psc=1'
#dia = str(date.today().day) + '/' + str(date.today().month) + '/' + str(date.today().year)

webdriver = webdriver.PhantomJS()
webdriver.get(url)    

while True:
    try:

        time.sleep(30)
        dia = datetime.now()
        
        preco = webdriver.find_element_by_id('priceblock_ourprice').text
        
        webdriver.delete_all_cookies()
        webdriver.execute_script('localStorage.clear();')
        
        webdriver.refresh()
        
        preco = float(preco[2:].replace('.','').replace(',','.'))
        
        arquivo = open('log_execucao_scrapper.txt','a+')
        
        if preco < 2100:
            envia_sms(preco)
            arquivo.write(f'[{dia}] - SMS ENVIADO - VALOR R${preco}\n')
            print(f'[{dia}] - SMS ENVIADO - VALOR R${preco}')
        elif preco >= 2100:
            arquivo.write(f'[{dia}] - VALOR MAIOR DO QUE ESPERADO - VALOR R${preco}\n')
            print(f'[{dia}] - VALOR MAIOR DO QUE ESPERADO - VALOR R${preco}')
        else:
            arquivo.write(f'[{dia}] - ERRO AO ENVIAR SMS - VALOR R${preco}\n')
            print(f'[{dia}] - ERRO AO ENVIAR SMS - VALOR R${preco}')
        
        arquivo.close()
    except:
        try:
            arquivo.close()
        except:
            pass
        
        arquivo = open('log_execucao_scrapper.txt','a+')
        arquivo.write(f'[{dia}] - ERRO NA CONSULTA - VALOR R${preco}\n')
        print(f'[{dia}] - ERRO NA CONSULTA - VALOR R${preco}')
        arquivo.close()
        
    time.sleep(3600)
