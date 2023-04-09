# Отчет о проделанной работе

1. Написал скрипт для загрузки котировок с Binance. Загрузил данные о часовых свечах для BTCRUB начиная с 2019 до сегодня.(Эта пара стала доступна на binance только в 2019) 


Код: [load_data.py](/load_data.py)
```
# Пример использования скрипта
$ load_data.py --symbol=BTCRUB --interval=1h
```

2. Провел базовую предобработку данных. Подобрал гиперпараметры и обучил LSTM модель. Модель по 72 прошлым часам делает прогноз цены на следующий час.

 Код: [train.ipynb](/train.ipynb)

metrics|open_price|high_price|low_price|close_price
---|---:|---:|---:|---:|
Std of prices|1412701|1420867|1403717|1412630
MAE Train|20631|21981|25080|24119
MAE Test|13684|14866|12360|14933


3. Разработал сервис на FastAPI который по get запросу возвращает предсказание стоимости валютной пары на следующий час.

Код: [web_app.py](/web_app.py)

```python
import requests

url = 'http://some_ip/predict_price_btcrub'
prediction = requests.get(url).json()

prediction
{'open_price': 2282917.5,
'high_price': 2293903.0,
'low_price': 2270617.0,
'close_price': 2283752.25}
```
