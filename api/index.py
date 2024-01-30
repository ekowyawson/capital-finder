import json
import requests
from urllib import parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        my_path = self.path
        url_components = parse.urlsplit(my_path)
        query_string_list = parse.parse_qsl(url_components.query)
        query_string_dict = dict(query_string_list)

        # Choose the appropriate handler based on the presence of 'country' or 'capital'
        if 'country' in query_string_dict:
            response = get_capital_by_country({'query': query_string_dict})
        elif 'capital' in query_string_dict:
            response = get_country_by_capital({'query': query_string_dict})
        else:
            response = {
                'statusCode': 400,
                'body': 'Invalid query parameters'
            }

        self.send_response(response['statusCode'])
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))
        return

# Endpoint for the Rest Countries API
API_URL = "https://restcountries.com/v3.1/"

def fetch_country_info(query_components):
    # Determine the API URL based on the query
    if 'country' in query_components:
        url = f"{API_URL}name/{query_components['country'][0]}"
    elif 'capital' in query_components:
        url = f"{API_URL}capital/{query_components['capital'][0]}"
    else:
        return None

    # Make a request to the external API
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def generate_response(query_components, country_info):
    if not country_info:
        return "No data available for the given input."

    response = ""
    for country in country_info:
        name = country['name']['common']
        capital = ', '.join(country['capital']) if 'capital' in country else 'No capital'
        currency = ', '.join(country['currencies'].keys()) if 'currencies' in country else 'No currency info'
        languages = ', '.join(country['languages'].values()) if 'languages' in country else 'No language info'

        if 'country' in query_components:
            response += f"The capital of {name} is {capital}. "
        elif 'capital' in query_components:
            response += f"{capital} is the capital of {name}. "

        response += f"The currency is {currency} and the languages are {languages}.\n"

    return response.strip()

def handler(req, res):
    # Parse query components from the request URL
    parsed_url = parse.urlparse(req.url)
    query_components = parse.parse_qs(parsed_url.query)

    # Fetch data from an external API
    country_info = fetch_country_info(query_components)

    # Generate response based on the query
    response = generate_response(query_components, country_info)

    # Send the response
    res.status(200).send(response)

# For Vercel, you typically export the handler function
exported_function = handler

def capital_finder(request):
    query_params = request.get('query', {})

    if 'country' in query_params:
        country = query_params['country']
        capital = get_capital_by_country(country)
        if capital:
            return {
                'statusCode': 200,
                'body': f'The capital of {country} is {capital}'
            }
        else:
            return {
                'statusCode': 404,
                'body': f'Capital not found for {country}'
            }
    elif 'capital' in query_params:
        capital = query_params['capital']
        country = get_country_by_capital(capital)
        if country:
            return {
                'statusCode': 200,
                'body': f'{capital} is the capital of {country}'
            }
        else:
            return {
                'statusCode': 404,
                'body': f'Country not found for {capital}'
            }
    else:
        return {
            'statusCode': 400,
            'body': 'Invalid query parameters'
        }

def get_capital_by_country(country):
    url = f'https://restcountries.com/v3.1/name/{country}?fields=name,capital'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data:
        capital = data[0]['capital'][0]
        return capital
    else:
        return None

def get_country_by_capital(capital):
    url = f'https://restcountries.com/v3.1/capital/{capital}?fields=name,capital'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data:
        country = data[0]['name']['common']
        return country
    else:
        return None

# For Vercel, you would export the function like this
exported_function = handler