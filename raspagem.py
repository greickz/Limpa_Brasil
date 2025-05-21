from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
caminho = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"
servico = Service(caminho)
opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--disable-gpu')
opcoes.add_argument('--window-size=1920,1080')
navegador = webdriver.Chrome(service=servico, options=opcoes)
url = 'https://www.limpabrasil.eucuidodomeuquadrado.org/eventos-antigos'
navegador.get(url)
time.sleep(5)
eventos = {'Campanha': []}

try:
    WebDriverWait(navegador, 10).until(
        ec.presence_of_all_elements_located((By.CLASS_NAME, 'property-card'))
    )
    cards = navegador.find_elements(By.CLASS_NAME, 'property-card')
    print(f'{len(cards)} eventos encontrados.\nColetando os dados...')
    for card in cards:
        try:
            titulo = card.find_element(By.CLASS_NAME, 'property-card-title').text.strip()
        except NoSuchElementException:
            titulo = 'N/A'
        try:
            data_e_hora = card.find_elements(By.CLASS_NAME, 'property-card-title')[1].text.strip()
        except NoSuchElementException:
            data_e_hora = 'N/A'
        try: 
            #campanha = card.find_element(By.XPATH, '//body//div[@class="property-card card"]//div[@class="property-card-box card-box card-block"]//div[@class="property-preview-footer  clearfix"]//div[@class="property-preview-f-left text-color-primary"]/span[@class="label label-default label-tag-warning"]/a').text.strip() # terminar a parte da campanha
            campanha = card.find_element(By.CLASS_NAME, 'property-preview-f-left').text.strip() # terminar a parte da campanha
        except NoSuchElementException:
            campanha = 'N/A'
        try:
            cidade_estado = card.find_element(By.CLASS_NAME, 'post_single_cat').text.strip()
        except NoSuchElementException:
            cidade_estado = 'N/A'
        # eventos['Título'].append(titulo)
        # eventos['Data e Hora'].append(data_e_hora)
        # eventos['Cidade e Estado'].append(cidade_estado)
        eventos['Campanha'].append(campanha)
except TimeoutException:
    print('Erro: os elementos não carregaram a tempo.')
navegador.quit()
df = pd.DataFrame(eventos)
df.to_excel('raspagem_limpa_brasil_teste.xlsx', index=False)
print(f'\nRaspagem finalizada! {len(df)}')
