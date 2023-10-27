import requests
import json
from config import KEYS, HEADERS


class APIException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'''Невозможно перевести одинаковые валюты {KEYS[base]}.''')

        try:
            quote_ticker = KEYS[quote]
        except KeyError:
            raise APIException(f'''Не удалось обработать валюту {quote}''')
        try:
            base_ticker = KEYS[base]
        except KeyError:
            raise APIException(f'''Не удалось обработать валюту {base}''')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'''Не удалось обработать количество {amount}''')

        url = f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"
        payload = {}
        headers = HEADERS
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.content)
        total_base = resp['result']
        return total_base


