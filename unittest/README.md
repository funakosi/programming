# Pythonでユニットテスト



## 概要

- WebAPIを使用して天気を取得するクラスに対してユニットテストを作成する
- クラスは通常版（逐次版）と並列処理版の２つ



## 実行方法

- Python3.6で動作確認を行っています

- テスト対象のスクリプトの確認

```bash
$ ./getOkinawaWeather.py
# 上で動かない場合は以下も試して下さい
$ python3 getOkinawaWeather.py
```

- テストスクリプトの確認

```bash
$ ./test_weather_class.py
471010 start
+ 都市= 沖縄県 那覇 の天気
| 今日の天気= 曇り
| 明日の天気= 曇時々雨
| 明後日の天気= 雨時々曇
471010 done

.471020 start
+ 都市= 沖縄県 名護 の天気
| 今日の天気= 雨
| 明日の天気= 曇時々雨
| 明後日の天気= 雨時々曇
471020 done

.
----------------------------------------------------------------------
Ran 2 tests in 0.714s

OK
```
