import requests
import json
from database import insert_country_rate, get_country

def get_population(record): return record['Population']

def get_top10_countries(endpoint):
    try:
        if endpoint == '/paises/top10':
            output = []

            data = requests.get('https://restcountries.com/v3.1/all?fields=name,population')
            
            if data.status_code != 200:
                payload = {'message': 'Invalid API call! Please check the resource requested.', 'status_code': 400}
                raise Exception(payload)
            else:
            
                response = data.json()

                for country in response:
                    output.append({'Country': country['name']['common'], 'Population': country['population']})

                output.sort(key=get_population, reverse=True)

                top_ten_countries = output[:10]

                for top_country in top_ten_countries:
                    country_result = get_country(top_country['Country'])

                    if country_result == None:
                        insert_country_rate(top_country['Country'], '')
                        top_country.update({'Likes': 0, 'Dislikes': 0})
                    else:
                        country_likes = country_result[2]
                        country_dislikes = country_result[3]
                        top_country.update({'Likes': country_likes, 'Dislikes': country_dislikes})
                
                return top_ten_countries

        else:
            payload = {'message': 'Invalid API call! Please check the resource requested.', 'status_code': 400}
            raise Exception(payload)
    except Exception as e:
        return str(e)

def get_country_by_name(endpoint, country):
    try:
        if endpoint == f'/paises/buscar?nome=':
            
            data = requests.get(f'https://restcountries.com/v3.1/name/{country}')

            if data.status_code != 200:
                payload = {'message': data.text, 'status_code': data.status_code}
                raise Exception(payload)
            
            response = data.json()
            found_country = get_country(country)

            if found_country == None:
                insert_country_rate(found_country['Country'], '')
            else:
                response.append({'Likes': 0, 'Dislikes': 0})

            return response
        else:
            payload = {'message': 'Invalid API call! Please check the resource requested.', 'status_code': 400}
            raise Exception(payload)
    except Exception as e:
        return str(e)

# def post_country_rating(endpoint, country, vote):
#     try:
#         if endpoint == f'/paises/avaliar':

#             data = get_country_by_name('/paises/buscar?nome=', country)

#             if data == ''