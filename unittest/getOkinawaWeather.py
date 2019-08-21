#!/usr/bin/python3
import aiohttp
import asyncio
import async_timeout
import requests
import json

class WeatherAPI:
    def __init__(self, city, data):
        self.city = city
        self.data = data
    
    @classmethod
    def exec(cls, city):
        print("{} start".format(city))
        res = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1?city={}".format(city))
        data = res.json()
        cls.display(city,data)
        return cls(city,data)
    
    @classmethod
    def display(cls, city, data):
        print("+ 都市=", data["title"])
        print("| 今日の天気=", data["forecasts"][0]["telop"])
        print("| 明日の天気=", data["forecasts"][1]["telop"])
        print("| 明後日の天気=", data["forecasts"][2]["telop"])
        print("{} done".format(city))
        print("")

class AsyncWeatherAPI:
    def __init__(self, city, data):
        self.city = city
        self.data = data
    
    @classmethod
    async def fetch(cls, session, city):
        print("{} start".format(city))
        async with async_timeout.timeout(10):
            async with session.get("http://weather.livedoor.com/forecast/webservice/json/v1?city={}".format(city)) as response:
                data = await response.json()
                await cls.display(city,data)
                return cls(city,data)
    
    @classmethod
    async def display(cls, city, data):
        async with async_timeout.timeout(10):
            print("+ 都市=", data["title"])
            print("| 今日の天気=", data["forecasts"][0]["telop"])
            print("| 明日の天気=", data["forecasts"][1]["telop"])
            print("| 明後日の天気=", data["forecasts"][2]["telop"])
            print("{} done".format(city))
            print("")
    
    @classmethod
    async def exec(cls, locations):
        async with aiohttp.ClientSession() as session:
            promises = [cls.fetch(session, city) for city in locations]
            await asyncio.gather(*promises)


if __name__ == '__main__':
    # 天気を調べたい都市の一覧 
    locations=["471020","471030","472000","473000","474010","474020"]

    print ("=== 通常処理（逐次処理）===")
    [WeatherAPI.exec(city) for city in locations]

    print ("=== 非同期処理 ===")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AsyncWeatherAPI.exec(locations))
