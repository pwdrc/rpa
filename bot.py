import os
import time
from datetime import datetime,date
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações gerais
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
base_url = "https://rpachallengeocr.azurewebsites.net/"
start_button_id = "start" 
table_id = "tableSandbox"
extracted_data_file = "invoices.csv"
next = 3

# Inicia a navegação
driver.get(base_url)

# Clica no botão de start
start_button = driver.find_element(By.ID, start_button_id)
start_button.click()

# Aguarda o carregamento da tabela
time.sleep(2)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))

# Extrai dados da tabela
table_data = []
while next > 0:
    rows = driver.find_elements(By.XPATH, f"//table[@id='{table_id}']/tbody/tr")

    for row in rows:
        
        # Espera até que o texto da célula esteja presente
        WebDriverWait(row, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "td"))).text
    
        # Encontra os elementos "células" da tabela
        cells = row.find_elements(By.TAG_NAME, "td")

        # Inicializa a variável de data para encontrar as notas vencidas
        check_date = datetime.strptime(cells[2].text, "%d-%m-%Y")
      
        # Adiciona somente as que estão vencidas ou vencendo hoje
        if check_date.date() <= date.today():
            table_data.append([
                cells[1].text,
                cells[2].text,
                cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
            ])

    # Resolve o problema de ter que "rolar" a página até "next" estar no campo de visão
    # driver.execute_script("arguments[0].scrollIntoView();", next_element)
    driver.execute_script("window.scrollTo(0, 0);")
    driver.execute_script("window.scrollTo(document.body.scrollWidth, 0);")
    next_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tableSandbox_next")))
    next_element.click()
    next = next - 1

# Imprime os dados da tabela (teste)
print(table_data)

# Escreve os dados no arquivo invoices.csv
with open(extracted_data_file, 'w', newline='') as file_csv:
    writer_csv = csv.writer(file_csv)

    writer_csv.writerow(["ID", "Due Date", "Invoice URL"])
    for line in table_data:
        writer_csv.writerow(line)

print(f'Arquivo "{extracted_data_file}" criado com sucesso.')

# Submete o invoices.csv
file_input = driver.find_element(By.NAME, "csv")
file_input.send_keys(os.path.abspath(extracted_data_file))

print(f'{extracted_data_file} submetido com sucesso')
print("se deu certo é outra história ¯\_(ツ)_/¯")

# time.sleep(120)
driver.quit()
