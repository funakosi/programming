# HTTP通信

- 色々な方法でHTTP通信を行う



## 準備

- Git for Windows のインストール
  - [公式サイト](https://gitforwindows.org/)からインストーラを入手しインストール
- jq のインストール
  - [公式サイト](https://stedolan.github.io/jq/)からダウンロードし保存した場所にパスを通す



## 一覧化

- この資料で説明する方法と使用するサイトの一覧を示す

| No   | 手法                   | livedoor api   | httpbin       |                | JSONPlaceholder |              |
| ---- | ---------------------- | -------------- | ------------- | -------------- | --------------- | ------------ |
|      |                        | GET            | GET           | POST           | GET             | POST         |
| 1    | curl                   | 1-livedoor-get | 1-httpbin-get | 1-httpbin-post | 1-place-get     | 1-place-post |
| 2    | java HttpURLConnection | 2-livedoor-get | 2-httpbin-get | 2-httpbin-post | 2-place-get     | 2-place-post |
| 3    | java Rest Assured      | 3-livedoor-get | 3-httpbin-get | 3-httpbin-post | 3-place-get     | 3-place-post |
| 4    | java OkHttp            | 4-livedoor-get | 4-httpbin-get | 4-httpbin-post | 4-place-get     | 4-place-post |

- 通信手段の説明

1. curl コマンドでデータを取得する方法を説明
2. Java 標準であるHttpURLConnectionを使用してデータを取得する方法を説明
3. Java のRest Assuredを使ってデータを取得する方法を説明
4. Java のOkHttpを使ってデータを取得する方法を説明

- 使用するサイトの説明

1. livedoor api

   お天気情報を取得できる[サイト](http://weather.livedoor.com/weather_hacks/webservice)

2. httpbin

   シンプルなHTTPリクエストとレスポンスを返してくれるサービス

3. JSONPlaceholder

   RESTで実装されたAPIサーバーです。ダミーデータを返却してくれる

