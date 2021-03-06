#!/usr/bin/python3
import unittest
from getOkinawaWeather import WeatherAPI

class Test_WeatherAPI(unittest.TestCase):

    def test_nage_weather(self):
        expected = "沖縄県 名護 の天気"
        actual = WeatherAPI.exec("471020")
        self.assertEqual(expected, actual.data["title"])

    def test_naha_weather(self):
        expected = "沖縄県 那覇 の天気"
        actual = WeatherAPI.exec("471010")
        self.assertEqual(expected, actual.data["title"])

if __name__ == "__main__":
    unittest.main()
