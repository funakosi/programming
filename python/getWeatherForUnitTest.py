#!/usr/bin/python3
import requests
import json
import unittest

class WeatherAPI:
    def __init__(self):
        self.base_url="http://weather.livedoor.com/forecast/webservice/json/v1"
        self.url=self.base_url+"?city={}"

    def exec(self, city):
        res = requests.get(self.url.format(city))
        data = res.json()
        return data

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        print ("setUp")
        self.weather = WeatherAPI()
    
    def testGetNahaWeather(self):
        print ("-- 那覇市の天気を取得 --")
        data = self.weather.exec("471010")
        self.assertEqual(data["title"],"沖縄県 那覇 の天気","title が間違っている。")
        self.assertEqual(data["location"]["prefecture"],"沖縄県","location-prefecture が間違っている。")
        self.assertEqual(data["location"]["area"],"沖縄","location-area が間違っている。")
        self.assertEqual(data["location"]["city"],"那覇","location-city が間違っている。")
        
    def tearDown(self):
        print ("tearDown")

if __name__ == '__main__':
    unittest.main()
