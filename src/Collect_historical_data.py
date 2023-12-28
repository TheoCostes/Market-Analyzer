import os
import requests
import ccxt
import pandas as pd

TIMEFRAME = '1d'

def fetch_top_cryptos(limit=500):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '6605bbe1-9a78-423c-964a-b0587763da34',
    }
    parameters = {
        'start': '1',
        'limit': str(limit),
        'sort': 'market_cap'
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    return [crypto['symbol'] for crypto in data['data']]

def fetch_ohlcv(exchange, crypto, timeframe='1d'):
    from_ts = exchange.parse8601('2010-07-21 00:00:00')
    ohlcv = exchange.fetch_ohlcv(f'{crypto}/USDT', timeframe, since=from_ts, limit=1000)
    return ohlcv

def save_to_csv(df, crypto, timeframe):
    if not os.path.exists(f'./data/{timeframe}'):
        os.makedirs(f'./data/{timeframe}')
    df.to_csv(f'./data/{timeframe}/{crypto}.csv', index=False)

def main():
    ex_binance = ccxt.binance()
    ex_bybit = ccxt.bybit()
    top_cryptos = fetch_top_cryptos()
    stable_list = ['USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'PAX', 'HUSD', 'GUSD',
                   'USDS', 'USDK', 'USN', 'USDP', 'USDQ', 'UST', 'USD', 'EURS',
                   'USDX', 'USDB', 'USDO', 'USDN', 'USDJ', 'USDU', 'USDG', 'USDR',
                   'USDI', 'USDM', 'USDH', 'USDSB', 'USDAP', 'USDSH', 'USDSN', 'USDSU',
                   'USDSX', 'USDSY', 'USDSZ', 'USDTZ', 'USDTT', 'USDTU', 'USDTW',
                   'USDTX', 'USDTY', 'USDTA', 'USDTB', 'USDTG', 'USDTI', 'USDTJ',
                   'USDTK', 'USDTL', 'USDTM', 'USDTP', 'USDTQ', 'USDTR', 'USDTV',
                   'USDTW', 'USDTX', 'USDTY', 'USDTZ', 'USDT0', 'USDT1', 'USDT2',
                   'USDT3', 'USDT4', 'USDT5', 'USDT6', 'USDT7', 'USDT8', 'USDT9',
                    'USDTA']
    ohlcv_list = []
    for crypto in top_cryptos:
        if crypto not in stable_list and f'{crypto}.csv' not in os.listdir(f'./data/{TIMEFRAME}'):
            from_ts = ex_binance.parse8601('2010-07-21 00:00:00')
            print(f'Fetching data for {crypto}')
            try:
                ohlcv = ex_binance.fetch_ohlcv(f'{crypto}/USDT', TIMEFRAME, since=from_ts, limit=1000)
                print("binance")
            except:
                try:
                    ohlcv = ex_bybit.fetch_ohlcv(f'{crypto}/USDT', TIMEFRAME, since=from_ts, limit=1000)
                    print("bybit")
                except:
                    print(f'no crypto {crypto} on binance or bybit')
                    continue
            ohlcv_list.append(ohlcv)
            while True:
                try:
                    from_ts = ohlcv[-1][0]
                except:
                    try:
                        from_ts = ex_binance.parse8601('2015-07-21 00:00:00')
                    except:
                        try:
                            from_ts = ex_binance.parse8601('2020-07-21 00:00:00')
                        except:
                            continue
                try:
                    new_ohlcv = ex_binance.fetch_ohlcv(f'{crypto}/USDT', TIMEFRAME, since=from_ts, limit=1000)
                except:
                    try:
                        new_ohlcv = ex_bybit.fetch_ohlcv(f'{crypto}/USDT', TIMEFRAME, since=from_ts, limit=1000)

                    except:
                        print(f'no crypto {crypto} on binance or bybit')
                        continue
                ohlcv.extend(new_ohlcv)
                if len(new_ohlcv) != 1000:
                    break
                # Convert to DataFrame
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                # Convert timestamp to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                save_to_csv(df, crypto, TIMEFRAME)

if __name__ == "__main__":
    main()
