import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неизвестная валюта  -  {base}, попробуйте снова')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неизвестная валюта -  {quote}, попробуйте снова')

        if quote == base:
            raise APIException(f'Введите различные валюты: {base}.')

        try:
            amount = float(amount)

        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        if amount < 0:
            raise APIException(f'Вы ввели отрицательное кол-во')

        #if base_ticker not in keys
            #raise APIException(f'Не удалось получить курс для валюты: {base}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base = total_base * amount
        return total_base
