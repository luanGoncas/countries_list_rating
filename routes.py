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
                raise Exception(data.text)
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
                
                payload = {'message': top_ten_countries, 'status_code': 200}

                return payload

        else:
            raise Exception('{"message": "Invalid API call! Please check the resource requested.", "status": 400}')
    except Exception as e:
        message = json.loads(str(e))
        payload = {'message': message['message'], 'status_code': message['status']}
        return payload

def get_country_by_name(endpoint, country):
    try:
        if endpoint == f'/paises/buscar?nome=':
            
            data = requests.get(f'https://restcountries.com/v3.1/name/{country}')

            if data.status_code != 200:
                raise Exception(data.text)
            
            response = data.json()
            found_country = get_country(response[0]['name']['common'])

            if found_country == None:
                insert_country_rate(found_country['Country'], '')
                response.append({'Likes': 0, 'Dislikes': 0})
            else:
                likes = found_country[2]
                dislikes = found_country[3]
                response.append({'Likes': likes, 'Dislikes': dislikes})

            payload = {'message': response, 'status_code': 200}

            return payload
        else:
            raise Exception('{"message": "Invalid API call! Please check the resource requested.", "status": 400}')
    except Exception as e:
        message = json.loads(str(e))
        payload = {'message': message['message'], 'status_code': message['status']}
        return payload

def post_country_rating(endpoint, country, vote):
    try:
        if endpoint == f'/paises/avaliar':

            data = get_country_by_name('/paises/buscar?nome=', country)

            if data['status_code'] != 200:
                raise Exception('{"message": "Invalid API call! Please check the resource requested.", "status": 400}')
            else:
                country_rated = data['message'][0]['name']['common']
                insert_country_rate(country_rated, vote)
                output = get_country_by_name('/paises/buscar?nome=', country)

                payload = {'message': output['message'], 'status_code': 200}
                return payload
    except Exception as e:
        message = json.loads(str(e))
        payload = {'message': message['message'], 'status_code': message['status']}
        return payload