# Obtenção de dados climáticos e armazenamento no Supabase.
Este código em Python utiliza a biblioteca requests para fazer requisições à API do OpenWeather e obter informações climáticas de várias cidades. Os dados são salvos em um arquivo JSON e também são inseridos em uma tabela no Supabase.
## _Pré-requisitos_
Antes de executar o código, certifique-se de ter instalado as seguintes bibliotecas Python:
- requests
- json
- datetime
- os
- supabase
- dotenv

Além disso, você precisará de uma chave de API do OpenWeather e das informações de configuração do Supabase, que serão lidas de um arquivo .env. Certifique-se de criar um arquivo .env no mesmo diretório do código e defina as seguintes variáveis:

```sh
API_KEY_OPENWEATHER=<sua chave de API do OpenWeather>
SUPABASE_URL=<URL do seu projeto do Supabase>
SUPABASE_KEY=<chave de acesso do Supabase>
```
## _Como usar o código_
1 - Importe as bibliotecas necessárias:

```py
import requests
import json
from datetime import datetime
import os
from supabase import create_client
from dotenv import load_dotenv
```
2 - Carregue as variáveis de ambiente do arquivo .env:
```py
load_dotenv()
API_KEY_OPENWEATHER = os.getenv("API_KEY_OPENWEATHER")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
```
3 - Defina as cidades desejadas e uma lista vazia para armazenar os dados:
```py
cidades = ["Ushuaia", "Harare", "Sydney", "Trondheim", "Wellington", "Nuuk", "Colombo", "Pamplemousses", "Yellowknife"]
lista_cidades = []
```
4 - Faça uma requisição API para buscar os dados climáticos de cada cidade e armazene-os em uma lista de dicionários:
```py
for cidade in cidades:
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY_OPENWEATHER}&lang=pt_br"
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()

    # Extrai as informações relevantes da resposta da API
    name = requisicao_dic['name']
    humidity = requisicao_dic['main']['humidity']
    description = requisicao_dic['weather'][0]['description']
    temp_kelvin = requisicao_dic['main']['temp']
    temp_celsius = temp_kelvin - 273.15
    temp_min_kelvin = requisicao_dic['main']['temp_min']
    temp_min_celsius = temp_min_kelvin - 273.15
    temp_max_kelvin = requisicao_dic['main']['temp_max']
    temp_max_celsius = temp_max_kelvin - 273.15

    # Cria um dicionário com os dados da cidade
    cidade_dict = {
        "name": name,
        "humidity": humidity,
        "description": description,
        "temp_celsius": temp_celsius,
        "temp_min_celsius": temp_min_celsius,
        "temp_max_celsius": temp_max_celsius
    }

    # Adiciona o dicionário à lista de cidades
    lista_cidades.append
```

5 - Salve os dados obtidos em um arquivo JSON:
```py
data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M")
nome_arquivo = f"dados_cidades_{data_atual}.json"

with open(nome_arquivo, "w") as f:
    json.dump(lista_cidades, f)
```
Isso criará um arquivo JSON com os dados das cidades, usando a data e hora atual como parte do nome do arquivo.

6 - Insira os dados na tabela do Supabase:
```py
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
```

Essa parte do código insere os dados obtidos na tabela "cidades" no Supabase, usando o cliente do Supabase.

Certifique-se de configurar corretamente as variáveis de ambiente API_KEY_OPENWEATHER, SUPABASE_URL e SUPABASE_KEY para garantir o funcionamento adequado do código.

Esse é um exemplo simples de como obter dados climáticos de várias cidades e armazená-los em um arquivo JSON e no Supabase. Sinta-se à vontade para personalizar e adaptar o código de acordo com suas necessidades.



