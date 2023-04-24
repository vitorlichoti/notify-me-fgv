import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from parsel import Selector
from twilio.rest import Client


def send_sms(num):
    account_sid = "AC0cd10c1130fb2e6913c2493f63f02cd5"
    auth_token = "02a43f48c82fbd07ccf36b8e56bc6a99"
    client = Client(account_sid, auth_token)
    client.messages.create(
        body="Chegou a horaaaa, abre a FGV aí https://conhecimento.fgv.br/concursos/rfb22",
        from_="+16813219510",
        to=f'+${num}'
    )
    print('SMS enviado')


def chegou_a_hora(num):
    BASE_URL = "https://web.whatsapp.com/"
    CHAT_URL = "https://web.whatsapp.com/send?phone={num}&text&type=phone_number&app_absent=1"
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")

    browser = webdriver.Chrome(
        options=chrome_options,
    )
    browser.get(BASE_URL)
    browser.maximize_window()
    message = 'Chegou a horaaaa, abre a FGV aí https://conhecimento.fgv.br/concursos/rfb22'
    browser.get(CHAT_URL.format(phone=num))
    time.sleep(3)
    inp_xpath = (
        '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    )
    input_box = WebDriverWait(browser, 60).until(
        expected_conditions.presence_of_element_located((By.XPATH, inp_xpath))
    )
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)
    time.sleep(5)


def url(num):
    html_content = requests.get("https://conhecimento.fgv.br/concursos/rfb22")
    selector = Selector(html_content.text)
    list_pdfs = selector.css('div.field.field--name-field-concurso-arquivos.field--type-entity-reference-revisions.field--label-above.field__items div.field__item')
    print(len(list_pdfs))
    if len(list_pdfs) > 141:
        send_sms(num)
        chegou_a_hora(num)
    else:
        print('not yet')
        time.sleep(10)
        url()


if __name__ == '__main__':
    num = int(input("Informe o número no qual deseja enviar a notificação: exemplo -> 556799345123 "))
    url(num)
