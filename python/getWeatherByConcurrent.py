#!/usr/bin/python3
import requests
import json
import unittest
from concurrent import futures
import time
import os
import aiohttp
import asyncio
import async_timeout

class WeatherAPIBase:
    def __init__(self):
        self.base_url="http://weather.livedoor.com/forecast/webservice/json/v1"
        self.url=self.base_url+"?city={}"

class WeatherAPI(WeatherAPIBase):
    def exec(self, city):
        res = requests.get(self.url.format(city))
        data = res.json()
        return data

class AsyncWeahterAPI(WeatherAPIBase):
    async def fetch(self, session, city):
        async with async_timeout.timeout(10):
            async with session.get(self.url.format(city)) as response:
                data = await response.json()
                await self.display(data)
                return data
    
    async def display(self, data):
        async with async_timeout.timeout(10):
            print(data["title"])
    
    async def exec(self, locations):
        async with aiohttp.ClientSession() as session:
            promises = [self.fetch(session, city) for city in locations]
            await asyncio.gather(*promises)

if __name__ == '__main__':
    # 天気を調べたい都市の一覧 
    locations=["471010","471020","471030","472000","473000","474010","474020"]
    # インスタンス化
    weather = WeatherAPI()
    
    # 通常処理
    print ("=== 通常処理（逐次処理）===")
    start = time.time()
    for city in locations:
        data = weather.exec(city)
        print (data["title"])
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(round(elapsed_time,2))+"[sec]")

    # 並行/並列処理
    print ("=== 並行/並列処理 ===")
    start = time.time()
    futureList = []
    with futures.ThreadPoolExecutor() as executor:
        for city in locations:
            future = executor.submit(fn=weather.exec, city=city)
            futureList.append(future)

    for future in futures.as_completed(futureList):
        data = future.result()
        print (data["title"])
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(round(elapsed_time,2))+"[sec]")

    # 非同期処理
    print ("=== 非同期処理 ===")
    start = time.time()
    asyncWeather = AsyncWeahterAPI()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncWeather.exec(locations))
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(round(elapsed_time,2))+"[sec]")
