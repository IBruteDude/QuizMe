
import random
from src.quote_data import quotes
import requests

class QuoteGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.api-ninjas.com/v1/quotes'

    def get_quote(self, category='happiness'):
        try:
            url = f'{self.base_url}?category={category}'
            headers = {'X-Api-Key': self.api_key}
            response = requests.get(url, headers=headers)

            if response.status_code == requests.codes.ok:
                quote = response.json()[0]['quote']
                author = response.json()[0]['author']
                return (quote,author)
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except:
            print('No response and data')
            return self.get_offline_quote()

    def get_offline_quote(self):
        random_quote = random.choice(quotes)
        print(random_quote)
        quote = random_quote['quote']
        author = random_quote['author']
        return (quote, author)

api_key = 'U7eIfzmzpGERGLafQ9EcCw==KXF70Lznn6T5qaQm'

quote_generator = QuoteGenerator(api_key)

category = 'happiness'

generated_quote = quote_generator.get_quote(category)

if generated_quote:
    print(f'Generated a {category} quote: {generated_quote[0]}, {generated_quote[1]}')
