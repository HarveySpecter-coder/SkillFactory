import json
import requests
from typing import Union

currencies = ('USD', 'RUB', 'EUR')


class APIException(Exception):
    pass


class SymbolPrice:
    @staticmethod
    def get_price(base: str, quote: str, amount: Union[float, int, str]) -> str:
        base = base.upper()
        quote = quote.upper()
        if base == quote:
            raise APIException('Нужно конвертировать разные валюты!')
        if base not in currencies or quote not in currencies:
            raise APIException('Введён неверный тикер!')
        try:
            float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        else:
            request = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}')
            request = json.loads(request.content)
            request = f'Стоимость {amount} {base} в {quote}: ' \
                      + str(round(float(request[quote]) * float(amount), 2))
            return request
