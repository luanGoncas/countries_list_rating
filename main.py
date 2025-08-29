import pprint
from routes import get_top10_countries, get_country_by_name, post_country_rating

# pprint.pprint(get_top10_countries('/paises/top10'))
# pprint.pprint(get_country_by_name('/paises/buscar?nome=', 'brazil'))
# pprint.pprint(post_country_rating('/paises/avaliar', 'china', 'dislike'))