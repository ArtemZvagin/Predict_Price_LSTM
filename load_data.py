import os
import time
from datetime import datetime
from typing import List

import fire 
import requests
import pandas as pd 

def get_data(symbol: str, start_time: int, 
              interval: str, limit: int=1000) -> List:
    
    url = "https://api.binance.com/api/v3/klines"
    params = {'symbol': symbol, 'startTime': start_time, 
              'interval': interval, 'limit': limit}

    data = requests.get(url, params=params)
    if data.status_code == 200:
        res = data.json()
        if res: 
            return res 
        # Если апи вернул пустой список, значит для этого времени еще нет свечей
        return ['end']
    else:
        return []
    
def load_all_data(symbol: str, interval: str) -> pd.DataFrame:
    # binance отрылся в 2017
    start_time = int(datetime.timestamp(datetime(year=2017, month=8, day=17)) * 1000)
    # Будем собирать все данные до этого дня
    end_time = int(datetime.timestamp(datetime.now())*1000)
    
    all_data = []   
    cnt_error = 0
    while start_time < end_time:
        data = get_data(symbol, start_time, interval)
        if data:
            # Если все доступные данные уже загружены, то выходим
            if data[0] == 'end':
                break
                
            all_data.extend(data)
            start_time = data[-1][6]
            cnt_error = 0
            
        else:
            # Сайт не ответил. Ждем 5 сек и пробуем еще раз
            time.sleep(5)
            cnt_error += 1
            # Если сайт не отвечает 5 раз, выходим из цикла
            if cnt_error == 5:
                print(f'Binance is not avaliable!!!')
                break
    
    return pd.DataFrame(data=all_data, 
                        columns=['open_time', 'open_price', 'high_price', 'low_price', 'close_price',
                                 'volume', 'close_time', 'quote_asset_volume', 'num_trades', 
                                 'base_asset_volume', 'buy_quote_asset_volume', 'unused_field'])

def main(symbol: str='BTCRUB', interval: str='1h'):

    folder = 'data/'
    if not os.path.isdir(folder):
        os.mkdir(folder)

    try:
        df = load_all_data(symbol=symbol, interval=interval)
        print(f'Loaded {df.shape[0]} rows. ')
        path = f'{folder}{symbol}.csv'
        df.to_csv(path, index=False)
        print(f'Data loaded to {path}')
        
    except Exception as _ex:
        print(_ex)


if __name__ == '__main__':
    fire.Fire(main)