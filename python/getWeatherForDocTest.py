#!/usr/bin/python3
import requests
import json

class WeatherAPI:
    def __init__(self):
        self.base_url="http://weather.livedoor.com/forecast/webservice/json/v1"
        self.url=self.base_url+"?city={}"

    def exec(self, city):
        res = requests.get(self.url.format(city))
        data = res.json()
        return data

def getOkinawaWeather(city):
    """沖縄の天気を取得する。

    >>> getOkinawaWeather("471010")
    沖縄県 那覇 の天気
    >>> getOkinawaWeather("471020")
    沖縄県 名護 の天気
    >>> getOkinawaWeather("474010")
    沖縄県 石垣島 の天気
    """
    weather = WeatherAPI()
    data = weather.exec(city) 
    print(data["title"])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
