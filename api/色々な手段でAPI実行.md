# 色々な手段でAPI実行

ここではcurlでAPIを実行し、取得した結果をjqコマンドで見やすく整形していく方法を説明していく。また、curu以外にもBashやPythonを用いてAPIを実行する方法にも言及していく。



## 準備

- WSL (Ubuntu) 環境で処理をすすめることを前提としているので、適宜環境構築をしておく

- jq コマンドは、`sudo apt install jq` でインストール可能



## 概要

- [livedoor天気情報](http://weather.livedoor.com/weather_hacks/webservice)で提供しているAPIを実行し、指定した地域の天気情報を取得し表示する

- パラメータで使用する値は全国の地点定義表に定義されている。上のリンク内にその旨も記載されているので確認しておく



## curlでAPI実行

- 以降の作業は、Ubuntuのターミナルで実行する

- 久留米(ID:400040)の天気を表示

  ```bash
  $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040
  ```

  - city={ここに各地点に対応するIDを指定}するだけなので実行するのはそれほど難しくはない



## jqで戻り値を見やすくする

- curlでの実行結果は改行等なにもないため少々見づらい
- jqコマンドを使用して結果を見やすくする（参考：[jqコマンドを使う日常のご紹介](https://qiita.com/takeshinoda@github/items/2dec7a72930ec1f658af))

1. 基本

   ```bash
   $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040 | jq
   ```

2. 地点の名前一覧を取得

   ```bash
   $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040 | jq ".pinpointLocations[].name"
   # -r付与でダブルクォーテーションを省くことができる
   $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040 | jq -r ".pinpointLocations[].name"
   ```

3. １つ目の地点の情報だけ表示

   ```bash
   $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040 | jq ".pinpointLocations[0]"
   ```

4. フィルターし再整形
   ３日間の天気予報だけを表示する

   ```bash
   $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040 | jq ".forecasts[] | {date:.dateLabel, telop: .telop}"
   ```

5. ３日間の天気をCSV形式で表示

   ```bash
   $ curl http://weather.livedoor.com/forecast/webservice/json/v1?city=400040 | jq -r ".forecasts[] | [.dateLabel, .telop] | @csv"
   ```



## BashでAPI実行

- これまでの実行方法をベースに、BashでAPIを実行してみる
- ここでは沖縄県の地区コードの一覧を配列として固定で所有し、それぞれの地区の値を引数にAPIを実行し、今日、明日、明後日の天気を表示する
- `$ vi getOkinawaWeather.sh`

```bash
#/bin/sh

# base url
url="http://weather.livedoor.com/forecast/webservice/json/v1?city="

# locations in okinawa
locations=(
  "471020"
  "471030"
  "472000"
  "473000"
  "474010"
  "474020"
)

# get each weather
for l in "${locations[@]}" ; do
  RESULT=$(curl -s ${url}${l})
  RET="${RESULT}"
  echo `echo ${RET} | jq -r '.title'`
  echo `echo ${RET} | jq -r '.forecasts[] | [.dateLabel, .telop]'`
done
```

- 実行権限を付与 `$ chmod +x getOkinawaWeather.sh`
- 実行すると以下のように各地区の天気を取得し表示する

```bash
$ ./getOkinawaWeather.sh
沖縄県 名護 の天気
[ "今日", "晴時々曇" ] [ "明日", "曇時々雨" ] [ "明後日", "曇時々雨" ]
沖縄県 久米島 の天気
[ "今日", "晴時々曇" ] [ "明日", "曇時々雨" ] [ "明後日", "曇時々雨" ]
沖縄県 南大東 の天気
[ "今日", "晴時々雨" ] [ "明日", "曇時々雨" ] [ "明後日", "曇時々雨" ]
沖縄県 宮古島 の天気
[ "今日", "晴のち曇" ] [ "明日", "曇時々雨" ] [ "明後日", "暴風雨" ]
沖縄県 石垣島 の天気
[ "今日", "晴れ" ] [ "明日", "曇時々雨" ] [ "明後日", "暴風雨" ]
沖縄県 与那国島 の天気
[ "今日", "晴れ" ] [ "明日", "曇のち雨" ] [ "明後日", "暴風雨" ]
```



## PythonでAPI実行

### 対話モードで実行してみる

```bash
$ python3
Python 3.6.8 (default, Jan 14 2019, 11:02:34)
[GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> r = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1?city=400040")
>>> import json
>>> data = json.loads(r.text)
>>> data       #dataの中身が表示される
...(省略)...
>>> print (data["title"])
福岡県 久留米 の天気
>>> print (data["pinpointLocations"])  #配列の中身が表示される
...(省略)...
>>> print (data["pinpointLocations"][0]["name"])
大牟田市
```



## スクリプトを作成し実行

- [こちら](https://qiita.com/shunyooo/items/b408b8d61f9f73b21da7)の記事を参考に実装

```python
#!/usr/bin/python3

import requests
import json

# 天気を調べたい都市の一覧 
locations=["471020","471030","472000","473000","474010","474020"]

# APIのひな型
api = "http://weather.livedoor.com/forecast/webservice/json/v1?city={city}"

# 各都市の温度を取得する
for location in locations:
    # APIのURLを得る
    url = api.format(city=location)
    # 実際にAPIにリクエストを送信して結果を取得する
    r = requests.get(url)
    # 結果はJSON形式なのでデコードする
    data = json.loads(r.text)    
    # 結果を出力
    print("+ 都市=", data["title"])
    print("| 今日の天気=", data["forecasts"][0]["telop"])
    print("| 明日の天気=", data["forecasts"][1]["telop"])
    print("| 明後日の天気=", data["forecasts"][2]["telop"])
    print("")
```

- 必要に応じて実行権限を付与し実行する
- 上のスクリプトをクラス化する

```python
#!/usr/bin/python3

import requests
import json

class WeatherAPI:
    def __init__(self, city, data):
        self.city = city
        self.data = data
    
    @classmethod
    def exec(cls, city):
        res = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1?city={}".format(city))
        data = res.json()
        # print (data)
        return cls(city, data)
    
    @classmethod
    def display(cls, data):
        print("+ 都市=", data["title"])
        print("| 今日の天気=", data["forecasts"][0]["telop"])
        print("| 明日の天気=", data["forecasts"][1]["telop"])
        print("| 明後日の天気=", data["forecasts"][2]["telop"])
        print("")

if __name__ == '__main__':
    # 天気を調べたい都市の一覧 
    locations=["471020","471030","472000","473000","474010","474020"]

    for location in locations:
        ret = WeatherAPI.exec(location)
        WeatherAPI.display(ret.data)
```

- 非同期処理でお天気情報を取得できるようにしてみる

```python
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

class AsyncWeahterAPI:
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
    loop.run_until_complete(AsyncWeahterAPI.exec(locations))
```

