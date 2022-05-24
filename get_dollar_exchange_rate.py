from pprint import pprint
import requests


def get_dollar():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return data['Valute']['USD']['Previous']
