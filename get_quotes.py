import random
from src.quote_data import quotes
import requests

class QuoteGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

        # this come form https://api-ninjas.com/api/quotes this site.
        self.base_url = 'https://api.api-ninjas.com/v1/quotes'

    def get_quote(self, category='happiness'):
        # get quote is fetch the quote form api
        # in category happiness by default
        try:
            url = f'{self.base_url}?category={category}'
            headers = {'X-Api-Key': self.api_key}
            # get( ) request fetch the data from api
            response = requests.get(url, headers=headers)
            # check of the staus of the code
            if response.status_code == requests.codes.ok:
                quote = response.json()[0]['quote']
                author = response.json()[0]['author']
                # this return the quote text and author of the quote
                return (quote.lower(),author)
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except:
            print('No response and data')
            # in the case of no internet will generate a random quote
            # from the src/quote_data file
            return self.get_offline_quote()

    def get_offline_quote(self):
        # generete a quote in case no internet in the device
        random_quote = random.choice(quotes)
        print(random_quote)
        quote = random_quote['quote']
        author = random_quote['author']
        return (quote.lower(), author)


# pass the api_key to class QuoteGenerator
api_key = 'U7eIfzmzpGERGLafQ9EcCw==KXF70Lznn6T5qaQm'
quote_generator = QuoteGenerator(api_key)

# select the category
category = 'happiness'
generated_quote = quote_generator.get_quote(category)

# test for development
if generated_quote:
    print(f'Generated a {category} quote: {generated_quote[0]}, {generated_quote[1]}')
