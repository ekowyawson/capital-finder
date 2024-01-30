import json
import requests
from urllib.parse import urlparse, parse_qs

API_URL = "https://restcountries.com/v3.1/"

def fetch_country_info(query_params):
    # Determine the API URL based on the query
    if 'country' in query_params:
        url = f"{API_URL}name/{query_params['country']}?fields=name,capital"
    elif 'capital' in query_params:
        url = f"{API_URL}capital/{query_params['capital']}?fields=name,capital"
    else:
        return None, 400, 'Invalid query parameters'

    response = requests.get(url)
    if response.status_code != 200:
        return None, response.status_code, 'Error fetching data'

    data = response.json()
    if not data:
        return None, 404, 'No data found'

    return data, 200, ''

def handler(request):
    query_params = parse_qs(urlparse(request.url).query)

    data, status_code, error_message = fetch_country_info(query_params)

    if status_code != 200:
        response_body = error_message
    else:
        # Generate the response
        if 'country' in query_params:
            country = data[0]['name']['common']
            capital = data[0]['capital'][0]
            response_body = f'The capital of {country} is {capital}'
        elif 'capital' in query_params:
            capital = data[0]['capital'][0]
            country = data[0]['name']['common']
            response_body = f'{capital} is the capital of {country}'
        else:
            response_body = 'Invalid query parameters'

    # Construct the HTTP response
    return json.dumps({
        'statusCode': status_code,
        'body': response_body
    })

# For Vercel, you would export the function like this
exported_function = handler