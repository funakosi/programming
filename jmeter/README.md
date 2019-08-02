# JMeterでAPI実行



JMeterを使用してAPIを実行する方法を示していく。以下の手順は基本的には[こちら](https://octoperf.com/blog/2018/04/23/jmeter-rest-api-testing/)のサイトに記載している内容をもとに作成したものです。



## インストール

- [ここ](https://jmeter.apache.org/)から最新版のJMeterをダウンロードしインストール
  - 事前にJavaがインストールされている必要あり（[参考したサイト](https://qiita.com/gorilla_gorilla_gorilla/items/f9837751b8914700fba0))



## 事前準備

- プラグインのインストール
  - [こちらのサイト](https://octoperf.com/blog/2017/03/09/how-to-extract-data-from-json-response-using-jmeter/)を参考に、JsonPath Pluginをインストールしておく
  - jarファイルをダウンロードして、`JMETER_HOME/lib/ext`に保存した後に JMeterを再起動する
- OctPerfのアカウント取得
  - [こちら](https://app.octoperf.com/#/access/signin)からアカウントを作成



## APIを実行する（簡易版）

1. リポジトリ内にあるサンプルファイル（*.jmx）をローカルに保存
2. JMeterを起動し、上で取得したファイルを開く
3. 左側のツリーで、Thread Group -> login 
4. 右側のパネルに表示されるパラメータ表で、username の値にログインで使用しているメールアドレスを、password の値にログインで使用するパスワードを指定する
5. ツールバー上の右向きの緑色▶をクリックし実行する
6. 結果は、ツリーの View Results Treeをクリックすると確認できる。ここで行っていることは以下
   1. loginでログインし、JSON Extractor で トークンを取得し変数tokenに保存
   2. getWrokspaces でワークスペースを取得。その際、headers に先ほど取得したトークンを指定
   3. JSON Assertion で取得したデータの1つ目の要素の名前が Defaultであることを確認する
   4. JSON Extractor でworkspaceIdと名前を取得
   5. getProjectsでワークスペース内にあるプロジェクト一覧を取得
      - パスの一部に４で取得したワークスペースIDを指定
      - headersにトークンを指定
7. Debug Samplerで変数等を確認
8. View Result Treeで結果を確認



## APIを実行する（詳細版）

[こちら](https://octoperf.com/blog/2018/04/23/jmeter-rest-api-testing/)のサイトに記載している手順に従って説明を記載

### 1. ログインしてトークンを取得

1. JMeter起動

2. Test Plan を右クリック > 追加 > Threads (User) > Thread Group
   名前を適当に入力（ここでは”API実行サンプル”と入力）

   ![1564726026725](.\resrouces\1564726026725.png)

3. API実行サンプルを右クリック > 追加 > サンプラー > Http リクエスト

4. 右側のパネルで必要な情報を入力
   パラメータ表の username と password に作成したアカウント情報を指定する

   ![1564726173301](.\resrouces\1564726173301.png)

5. Test Planを右クリック > 追加 > リスナー > 結果をツリーで表示

6. ツールバーの▶で実行する。トークンが取得できたことが確認できる
   ![1564726421668](.\resrouces\1564726421668.png)

### 2. トークンを抽出

- トークンを変数に保存し、後工程で使用できるようにする

1. login を右クリック > 追加 > 後処理 > JSON Extractor

2. 右側のパネルで必要な情報を入力

   ![1564726701507](.\resrouces\1564726701507.png)

3. 変数をデバッグできるように Debug Sampler を追加

4. API実行サンプルを右クリック > 追加 > サンプラー > Debug Sampler

5. ▶で実行して token が変数に保存されていることを確認

### 3.  ワークスペースの取得

1. HTTP リクエストを追加し必要な情報を入力

   ![1564727399159](.\resrouces\1564727399159.png)

2. 追加 > 設定エレメント > Http ヘッダマネージャを追加し先ほど取得したトークンを指定

   ![1564727439860](.\resrouces\1564727439860.png)

3. ここでは JSON Assertionを追加して値のチェックも行っている

   追加 > アサーション > JSON Assertion

   ![1564727604571](.\resrouces\1564727604571.png)

4. JSON Extractor で ワークスペースIDを取得している

   ![1564727669322](.\resrouces\1564727669322.png)

5. 実行するとワークスペースIDが変数に保存されていることが確認できる

   ![1564727851834](.\resrouces\1564727851834.png)

### 4. プロジェクトの一覧を取得

1. Httpリクエストを追加し必要な情報を入力
   パスの一部に取得したワークスペースIDを指定していることに注意
    `/design/projects/by-workspace/${workspaceId}/DESIGN`
2. Httpヘッダーマネージャも忘れずに設定
3. 実行するとプロジェクトの一覧が取得できる