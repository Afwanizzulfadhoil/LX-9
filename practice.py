import requests

api_key = '186a0412-f43c-454c-a711-6c61bf5d6fb6'

word = 'carbon'

root_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json'

final_url = f'{root_url}/{word}?key={api_key}'

r = requests.get(final_url)

definitions = r.json()

for definition in definitions:
    print(definitions)