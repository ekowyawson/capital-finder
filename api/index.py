import requests
from urllib import parse
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        my_path = self.path
        url_components = parse.urlsplit(my_path)
        query_string_list = parse.parse_qsl(url_components.query)
        query_string_dict = dict(query_string_list)

        if 'country' in query_string_dict:
            response = requests.get(f'https://restcountries.com/v3.1/name/{query_string_dict["country"]}?fields=name,capital')
            country_list = response.json()
            country_obj = country_list[0]
            capital = country_obj['capital'][0]
            message = f'The capital of {country_obj["name"]["common"]} is {capital}'
        elif 'capital' in query_string_dict:
            response = requests.get(f'https://restcountries.com/v3.1/capital/{query_string_dict["capital"]}?fields=name,capital')
            capital_list = response.json()
            capital_obj = capital_list[0]
            country = capital_obj['name']['common']
            message = f'{query_string_dict["capital"]} is the capital of {country}'

        else:
            message = 'Invalid query parameters'
            response = {
                'statusCode': 400,
                'body': 'Invalid query parameters'
            }
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
        return