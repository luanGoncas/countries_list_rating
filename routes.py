import requests
import pprint

def get_population(record): return record['Population']

def get_top10_countries(endpoint):
    try:
        if endpoint == '/paises/top10':
            output = []

            data = requests.get('https://restcountries.com/v3.1/all?fields=name,population')
            response = data.json()

            for country in response:
                output.append({'Country': country['name']['common'], 'Population': country['population']})

            output.sort(key=get_population, reverse=True)

            return output[:10]
        else:
            raise Exception('Invalid API call! Please check the resource requested.')
    except Exception as e:
        return str(e)

def get_country_by_name(endpoint, country):
    try:
        print('Endpoint:', endpoint)
        print('Country:', country)
        print(endpoint + country)
        if endpoint == f'/paises/buscar?nome=':
            
            data = requests.get(f'https://restcountries.com/v3.1/name/{country}')
            response = data.json()

            return response
        else:
            raise Exception('Invalid API call! Please check the resource requested.')
    except Exception as e:
        return str(e)

# pprint.pprint(get_top10_countries('/paises/top10'))