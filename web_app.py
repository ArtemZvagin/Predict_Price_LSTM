import pickle
from datetime import datetime 
from typing import List
import requests
import numpy as np
from fastapi import FastAPI
import uvicorn


last_data = [datetime.now().hour - 1, {}]
features = ['open_price', 'high_price', 'low_price', 'close_price']
app = FastAPI()

with open('data/predict.bin', 'rb') as file:
    func = pickle.load(file)

def get_data(symbol: str, start_time: int=None, 
              interval: str='1h', limit: int=72) -> List:
    
    url = "https://api.binance.com/api/v3/klines"
    params = {'symbol': symbol, 'startTime': start_time, 
              'interval': interval, 'limit': limit}

    data = requests.get(url, params=params)
    if data.status_code == 200:
        res = data.json()
        return [el[1:5] for el in res]
    else:
        return []

@app.get('/predict_price_btcrub')
async def get_price():
    global last_data
    # Если в этот час мы уже считали, то просто возвращаем
    if datetime.now().hour == last_data[0]:
        return last_data[1]
    
    try:
        data = get_data('BTCRUB')
    except Exception as _ex:
        return {'Error during load data from binance': str(_ex)}
    
    try:       
        pred = func(np.array(data))
        pred = {features[i]: float(pred[i]) for i in range(len(pred))}
        last_data = [datetime.now().hour, pred]
        return pred
    except Exception as _ex:
        return {'Error during predict': str(_ex)}
    



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
