import requests
import json
from datetime import datetime
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
API_KEY_OPENWEATHER = os.getenv("API_KEY_OPENWEATHER")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M")
cidades = ["Ushuaia", "Harare", "Sydney", "Trondheim", "Wellington","Nuuk","Colombo","Pamplemousses","Yellowknife"]

lista_cidades = []

# Faz a requisição API para buscar os dados da cidade
for cidade in cidades:
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY_OPENWEATHER}&lang=pt_br"
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()

    name = requisicao_dic['name']
    humidity = requisicao_dic['main']['humidity']
    description = requisicao_dic['weather'][0]['description']
    temp_kelvin = requisicao_dic['main']['temp']
    temp_celsius = temp_kelvin - 273.15
    temp_min_kelvin = requisicao_dic['main']['temp_min']
    temp_min_celsius = temp_min_kelvin - 273.15
    temp_max_kelvin = requisicao_dic['main']['temp_max']
    temp_max_celsius = temp_max_kelvin - 273.15

    cidade_dict = {
        "name": name,
        "humidity": humidity,
        "description": description,
        "temp_celsius": temp_celsius,
        "temp_min_celsius": temp_min_celsius,
        "temp_max_celsius": temp_max_celsius
    }

    lista_cidades.append(cidade_dict)

# Salva os dados em um arquivo JSON   
data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M")
nome_arquivo = f"dados_cidades_{data_atual}.json"

with open(nome_arquivo, "w") as f:
    json.dump(lista_cidades, f)


# Insere os dados na tabela
table = 'cidades'
dados = [
    {
        'name': cidade['name'],
        'humidity': cidade['humidity'],
        'description': cidade['description'],
        'temp_celsius': cidade['temp_celsius'],
        'temp_min_celsius': cidade['temp_min_celsius'],
        'temp_max_celsius': cidade['temp_max_celsius'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    } for cidade in lista_cidades
]
resultado = supabase_client.table(table).insert(dados).execute()