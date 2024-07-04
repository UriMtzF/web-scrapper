import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

from bs4 import BeautifulSoup

load_dotenv()
USER = os.getenv('username')
PWD = os.getenv('password')

chromedriver_path = '/home/umartinez/Applications/ChromeDriver/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# driver = webdriver.Chrome(executable_path=path, options=options)
driver = webdriver.Chrome(executable_path=chromedriver_path)

try:
  driver.maximize_window()
  
  driver.get('https://www.sita.uaemex.mx/tutoria/indexTUTOR.php')
  
  WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, 'pwd')))
  
  username_input = driver.find_element_by_id('user')
  password_input = driver.find_element_by_id('pwd')
  
  username_input.send_keys(USER)
  password_input.send_keys(PWD)
  password_input.send_keys(Keys.RETURN)
  
  enter_tutor_element = WebDriverWait(driver=driver, timeout=10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), ' TRABAJAR CON ESTE GRUPO')]"))
  )
  
  enter_tutor_element.click()
  
  WebDriverWait(driver=driver, timeout=10).until(
    lambda d: d.execute_script('return document.readyState') == 'complete'
  )
  
  students_page = driver.page_source
  
  soup = BeautifulSoup(students_page, 'html.parser')
  
  students_table = soup.find('table', {'id': 'tblToExcl'})
  
  hrefs = []
  
  if students_table:
    links = students_table.find_all('a', href=True)
    
    for link in links:
      acc_num = link.get_text()
      if acc_num.isdigit() and len(acc_num) == 7:
        hrefs.append(link['href'])
  else:
    print("No se encontró la tabla")
  
  file_index = 0
  for href in hrefs:
    driver.get('https://www.sita.uaemex.mx/tutoria/tutor/' + href)
    
    button_seguimiento = WebDriverWait(driver=driver, timeout=10).until(
      EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Seguimiento académico')]"))
    )
    button_seguimiento.click()
    
    button_trayectoria = driver.find_element_by_xpath("//a[contains(text(), 'Trayectoria académica')]")
    button_trayectoria.click()
    
    WebDriverWait(driver=driver, timeout=10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "Estilo24"))
    )
    
    html_source = driver.page_source
    
    file_index += 1
    
    if not os.path.exists("htmls"):
      os.makedirs("htmls")
    with open("htmls/trayectoria" + str(file_index) + ".html", 'w', encoding='utf-8') as file:
      file.write(html_source)
finally:
  driver.quit()