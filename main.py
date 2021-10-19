import requests
from twilio.rest import Client


STOCK_NAME = "AAPL"
COMPANY_NAME = "apple"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api = 'ETYD3N7ZZKU9NQLE'

NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"
news_api = 'b9cec28efb9849f4b8cc013b643fde68'

account_sid = 'AC747614aefb2a77f9501c3efbb57457ef'
auth_token = '72399bd399a264728d7fa5d0eb171630'

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': stock_api
}
respond = requests.get(STOCK_ENDPOINT, params=stock_params)
data = respond.json()
data_dict = data["Time Series (Daily)"]
data_list = [value for (key,value) in data_dict.items()]
closing_data_yes = float(data_list[0]['4. close'])
closing_data_bef_yes = float(data_list[1]['4. close'])

difference = round((closing_data_yes/closing_data_bef_yes)*100 - 100,2)


if difference >=1 or difference<=- 1:
    news_params = {
        'apiKey': news_api,
        'country': 'us',
        'q': COMPANY_NAME
    }
    r = requests.get(NEWS_ENDPOINT,params=news_params)
    data_news = r.json()["articles"]
    three_articles = data_news[:3]

    if difference >= 0:
        article_list = [f"AAPL: 🔺{difference}% \nHedline: {i['title']}.\n Brief: {i['description']}" for i in three_articles]
    elif difference < 0:
        article_list = [f"AAPL: 🔻{difference}% \nHedline: {i['title']}.\n Brief: {i['description']}" for i in three_articles]

    for article in article_list:
        client = Client(account_sid, auth_token)
        message = client.messages \
                        .create(
                             body=f"{article}",
                             from_='+14123856885',
                             to='+998993727053'
                         )
