from binance.spot import Spot
import re
import redis
from websockets.sync.client import connect
import json


class Courses:
    _ws = connect(uri='wss://ws-api.binance.com/ws-api/v3')
    _r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @classmethod
    def _connect(cls):
        try:
            cls._ws.ping()
        except:
            cls._ws = connect(uri='wss://ws-api.binance.com/ws-api/v3')

    @classmethod
    def _get_courses_from_api(cls):
        cls._connect()
        cls._ws.send('''{
              "id": "93fb61ef-89f8-4d6e-b022-4f035a3fadad",
              "method": "ticker",
              "params": {
                "symbols": [
                "USDTRUB",
                "BTCRUB",
                "ETHRUB",
                "SOLRUB",
                "BTCUSDT",
                "ETHUSDT",
                "SOLUSDT"]
              }
            }''')
        message = cls._ws.recv()
        return message

    @classmethod
    def get_courses(cls):
        raw_response = cls._get_courses_from_api()
        response = json.loads(raw_response)
        data = {
            'USDT': {'USDT': 1},
            'BTC': {},
            'ETH': {},
            'SOL': {}
        }
        # pprint(response)
        for course in response['result']:
            match = re.match(r'(?P<cur>\w*)(?P<type>USDT|RUB)', course['symbol'])
            currency = match.group('cur')
            price_type = match.group('type')
            data[currency][price_type] = round(float(course['weightedAvgPrice']), 2)
            if price_type == 'RUB':
                data[currency]['volume'] = round(float(course['volume']), 2)
                data[currency]['quote_volume'] = round(float(course['quoteVolume']), 2)
                data[currency]['change'] = round(float(course['priceChange']), 2)
        data['KPFU'] = {
            'USDT': 4,
            'RUB': 4 * data['USDT']['RUB'],
            'volume': 4344,
            'quote_volume': round(4344 * 4 * data['USDT']['RUB'], 2)
        }
        result = json.dumps(data)
        cls._r.set('courses', result)
        return result

    @classmethod
    def get_cached_courses(cls):
        return json.loads(cls._r.get('courses'))
