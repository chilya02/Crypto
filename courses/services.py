from binance.spot import Spot
import re
def get_courses_from_api() -> dict:
    client = Spot()
    response = client.ticker_24hr(symbol=None, symbols=["USDTRUB", "BTCRUB", "ETHRUB", "SOLRUB", "BTCUSDT", "ETHUSDT", "SOLUSDT"], type="FULL")
    data = {
        'USDT': {'USDT': 1},
        'BTC': {},
        'ETH': {},
        'SOL': {}
        }
    for course in response:
        match = re.match(r'(?P<cur>\w*)(?P<type>USDT|RUB)', course['symbol'])
        currency = match.group('cur') 
        price_type = match.group('type')
        data[currency][price_type] = round(float(course['weightedAvgPrice']), 2)
        if price_type == 'RUB':
            data[currency]['volume'] = round(float(course['volume']), 2)
            data[currency]['quote_volume'] = round(float(course['quoteVolume']), 2)
            data[currency]['change'] = round(float(course['priceChange']), 2)
    return data