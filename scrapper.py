import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

load_dotenv()
USER = os.getenv('username')
PWD = os.getenv('password')

path = '/home/umartinez/Applications/ChromeDriver/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# driver = webdriver.Chrome(executable_path=path, options=options)
driver = webdriver.Chrome(executable_path=path)

try:
  driver.maximize_window()
  
  driver.get('https://www.sita.uaemex.mx/tutoria/indexPRUEBA.php')
  
  WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'pwd')))
  
  username_input = driver.find_element_by_id('user')
  password_input = driver.find_element_by_id('pwd')
  
  username_input.send_keys(USER)
  password_input.send_keys(PWD)
  password_input.send_keys(Keys.RETURN)
  
  driver.get('https://www.sita.uaemex.mx/tutoria/alumno/exani2_v14BALU.php')
  
  WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'cajita')))
  
  page_source = driver.page_source
  
  with open('scrape.html', 'w') as file:
    file.write(page_source)
finally:
  driver.quit()