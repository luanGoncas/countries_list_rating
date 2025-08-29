import pprint
from routes import get_top10_countries, get_country_by_name

pprint.pprint(get_top10_countries('/paises/top10'))
# pprint.pprint(get_country_by_name('/paises/buscar?nome=', 'china'))