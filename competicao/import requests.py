"""
import requests

# Substitua 'YOUR_API_KEY' pela chave de API que você obteve do OpenWeatherMap.
api_key = 'a665cc36552b1a4c7cdadc277f48ab13'

# Defina a cidade e o país (Braga, Portugal).
city = 'Braga'
country = 'pt'

# Faça a solicitação para obter os dados de nascer e pôr do sol.
url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID={api_key}'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    print(f'Hora do Nascer do Sol: {sunrise}')
    print(f'Hora do Pôr do Sol: {sunset}')
else:
    print(response.json())
    print('Falha na solicitação da API.')

    """

from bs4 import BeautifulSoup
import re
import pandas as pd

# HTML de entrada

meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# Crie a lista de nomes de arquivo diretamente com extensão .html
files = [f'files_html/{mes}.html' for mes in meses]

data = []
dias=[]
sunrises=[]
sunsets=[]

for file_name in files:
    f= open(file_name, 'r', encoding='utf-8')
    html = f.read()
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Selecionar a tabela
    table = soup.find('tbody')


    # Iterar sobre as linhas da tabela
    for row in table.find_all('tr'):
        # Extrair as informações relevantes
        #date = row.find('time').text
        date=""
        element = row.find_all('time')[1]
        datetime_value = element.get('datetime')

        pattern = r'(\d{2}-\d{2})T(\d{2}:\d{2})'

        # Use re.search() para encontrar as correspondências no valor datetime
        match = re.search(pattern, datetime_value)

        # Se houver uma correspondência, extraia os grupos
        if match:
            dia = match.group(1)  # "11-28"
            sunrise = match.group(2)  # "07:37"

        pattern = r'(\d{2}):(\d{2})'
        match = re.search(pattern, sunrise)
        if int(match.group(2))>0:
            sunrise=int(match.group(1))+1
        else:
            sunrise=int(match.group(1))
        

        sunset = row.find_all('time')[2].text

        match = re.search(pattern, sunset)
        if int(match.group(2))>0:
            sunset=int(match.group(1))+1
        else:
            sunset=int(match.group(1))

        dias.append(dia)
        sunrises.append(sunrise)
        sunsets.append(sunset)
            # Adicionar as informações à lista de dados

data = pd.DataFrame({'Dia': dias, 'Sunrise': sunrises, 'Sunset': sunsets })

# Save the data to a CSV file
#print(predict)
data.to_csv('data.csv', index=False)

print("Arquivo CSS criado com sucesso!")