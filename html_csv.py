import pandas as pd
from bs4 import BeautifulSoup

# Leer el archivo HTML local
html_file = r'source.html'
with open(html_file, 'r', encoding='utf-8') as file:
    html = file.read()

# Parsear el HTML
soup = BeautifulSoup(html, 'html.parser')

# Buscar la tabla que contiene el texto "TRAYECTORIA ESCOLAR"
tables = soup.find_all('table')
parent_table = None
for table in tables:
    header = table.find('div', class_='letras_negrita')
    if header and "TRAYECTORIA ESCOLAR" in header.text:
        parent_table = table
        break
    
target_table = None

# Si existe la tabla busca la primer tabla hijo
if parent_table:
    child_tables = parent_table.find_all('table')
    
    if child_tables:
        target_table = child_tables[0]
else:
    print("Tabla no encontrada")

# Verificar si la tabla fue encontrada
if target_table:
    # Extraer los datos de la tabla
    rows = target_table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        row_data = [ele.get_text(separator=' ').strip() for ele in cols]
        data.append(row_data)
else:
    print("No se encontró la tabla con el texto especificado.")

df = pd.DataFrame(data[1:], columns=data[0])

csv_file = r'data.csv'

df.to_csv(csv_file, index=False)