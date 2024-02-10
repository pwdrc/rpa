import os
import time
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

# Inicia a navegação
driver.get(base_url)
start_button = driver.find_element(By.ID, start_button_id)
start_button.click()

# Aguarda o carregamento da tabela
time.sleep(10)

# Extrai dados da tabela
table_data = []
next = 3
while(next > 0):
    time.sleep(1)
    rows = driver.find_elements(By.XPATH, f"//table[@id='{table_id}']/tbody/tr")

    for row in rows:
        # Espera até que o texto da célula esteja presente
        cell_text = WebDriverWait(row, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "td"))).text
    
        # Adiciona dados à tabela apenas se o texto da célula não estiver vazio
        if cell_text:
            cells = row.find_elements(By.TAG_NAME, "td")
            table_data.append({
                "ID": cells[1].text,
                "Due Date": cells[2].text,
                "Invoice URL": cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
            })
    next_element = driver.find_element(By.CLASS_NAME, "next")
    next_element.click()
    next = next - 1

# Imprime os dados da tabela
print(table_data)


# Aguarda X segundos antes de fechar
time.sleep(10)
driver.quit()
