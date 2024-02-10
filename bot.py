import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações gerais
driver = webdriver.Chrome()
base_url = "https://rpachallengeocr.azurewebsites.net/"
start_button_id = "start" 
table_id = "tableSandbox"
extracted_data_file = "invoices.csv"

# Inicia a navegação
driver.get(base_url)
start_button = driver.find_element(By.ID, start_button_id)
start_button.click()

# Aguarda o carregamento da tabela
time.sleep(3)

# Extrai dados da tabela
table_data = []
next = 3
while(next > 0):
    #time.sleep(1)
    rows = driver.find_elements(By.XPATH, f"//table[@id='{table_id}']/tbody/tr")

    for row in rows:
        # Espera até que o texto da célula esteja presente
        cell_text = WebDriverWait(row, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "td"))).text
    
        # Adiciona dados à tabela apenas se o texto da célula não estiver vazio
        if cell_text:
            cells = row.find_elements(By.TAG_NAME, "td")
            table_data.append([
                cells[1].text,
                cells[2].text,
                cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
            ])
    next_element = driver.find_element(By.CLASS_NAME, "next")
    next_element.click()
    next = next - 1

# Imprime os dados da tabela
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

# Aguarda X segundos antes de fechar
time.sleep(10)
driver.quit()
