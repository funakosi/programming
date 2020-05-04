# Real World HTTP
## 1.HTTP/1.0の世界

### 基本となる4つの要素
- メソッドとパス
- ヘッダー
- ボディ
- ステータス

### HTTP/0.9
- ボディの受信とパスのみ

### HTTP/1.0

```
curl --http1.0 http://localhost:18888/greeting
curl --http1.0 --get --data-urlencode "search word" http://localhost:18888
curl -v --http1.0 http://localhost:18888/greeting

curl --http1.0 -H "X-Test: Hello" http://localhost:18888
curl -v --http1.0 -A "Mozilla/5.0 (compatible; MSIE; Windows NT 6.1; Trident/6.0)" http://localhost:18888
```

- URLの構造
```
p.26 urlの構造
http://www.oreilly.co.jp/index.shtml

スキーム://ホスト名/パス

スキーム
 http:80, https:443, mailto..
 スキーム毎にデフォルトポート有
```

 ```
curl -X GET --data "hello=world" http://localhost:18888
 ```
## 2. HTTP/1.0ブラウザの基本機能の裏側
### 2-1. フォームの送信
- x-www-form-urlencoded
```
curl --http1.0 --data-urlencode title="Head First PHP & MySQL" --data-urlencode author="Lynn, Michael" http://localhost:18888
```
### 2-2. フォームを使ったファイル送信
- multipart/form-data
```
curl --http1.0 -F attachment-file=@test.txt http://localhost:18888
```

### 2-4. 圧縮
```
curl --http1.0 --compressed http://localhost:18888
```

### 2-6. BASIC認証とDIGEST認証
```
curl --http1.0 --basic -u user:pass http://localhost:18888
```

### 2-7. プロキシ
```
curl --http1.0 -x http://localhost:18888 -U user:pass http://example.com/helloworld
```

## 3. GOでHTTPクライアント

### 3-5. GET+Query
```
curl -G --data-urlencode "query=hello world" http://localhost:18888
```

### 3-6. HEAD
```
curl --head http://localhost:18888
```

### 3-7. x-www-form-urlencoded POST
```
curl -d test=value http://localhost:18888
```

### 3-8. POSTで任意のボディ送信
```
curl -T main.go -H "Content-Type: text/plain" http://localhost:18888
```

### 3-9. multipart/form-data
```
curl -F "name=Michael Jackson" -F "thumnail=@photo.jpg" http://localhost:18888
```

### 3-10. 自由なメソッドの送信
```
curl -X DELETE http://localhost:18888
```

### 3-15. タイムアウト
```
curl -m 2 http://localhost:8080/slow_page
```

## 4. HTTP/1.1のシンタックス

- 通信の高速化
  - Keep-Aliveがデフォルトで有効
- TLSによる暗号化通信のサポート
- 新メソッドの追加
  - PUT,DELETEが必須のメソッドになった
  - OPTION,TRACE,CONNECTメソッドが追加
- プロトコルのアップグレード
- 名前を使ったバーチャルホストのサポート
- サイズが事前にわからないコンテンツのチャンク転送エンコーディングのサポート
- DATA URIスキーム

### 4-4-3. CONNECT
```
> docker run -d -p 3128:3128 --name squid poklet/squid
> curl --proxy http://localhost:3128 -v https://yahoo.com
```

## 5. HTTP/1.1 セマンティックス

- ファイルのダウンロード（ファイル名指定）
- ダウンロードの中断・再開（範囲アクセス）
- XMLHttpRequest
- Geo-Location
- X-Powered-By
- リモートプロシージャコール
- WebDAV
- ウェブサイト間で共通の認証・認可プラットフォーム

### 5.3 XMLHttpRequest
- 今まで紹介してきた curl コマンドに相当する機能を JavaScript から使えるようにするのが XMLHttpRequest

#### 5-3-2. XMLHttpRequest とブラウザのHTTPリクエストの違い
- 送受信時にHTMLの画面がフラッシュ（リロード）されない
- メソッドとして、GETとPOST以外も送信できる
- フォームの場合、キーと値が1:1になっている形式のデータしか送信できず、レスポンスはブラウザで表示されてしまうが、プレーンテキスト、JSON、バイナリデータ、XMLなどのさまざまなフォーマットが送受信できる
- いくつか、セキュリティのための制約がある

### 5-6. リモートプロシージャコール(RPC)
- リモートプロシージャコールとは、別のコンピュータにある機能を、あたかも自分のコンピュータ内であるかのように呼び出しを行い、必要に応じて返り値受け取る仕組み。リモートメソッド呼び出し(RMI:Remote Method Invocation)と呼ばれることもある。

#### 5-6-1. XML-RPC
- 送信に使うメソッドはPOSTで、呼び出しの引数、返り値ともにXMLで表現するのでContent-Typeは常にtext/xml。GETはキャッシュされてしまう可能性があるため、RPC通信には不向き。

#### 5-6-2. SOAP
- SOAPはXML-RPCを拡張して作られた規格。
- SOAPは単なるRPCだったXML-RPCよりも複雑になっている。SOAPそのものはデータ表現フォーマットで、SOAPの企画の中にSOAPを使ったRPCであるSOAP-RPCも定義されている。

#### 5-6-3. JSON-RPC
- JSON-RPCは、XML-RPCのXMLの代わりにJSONを使ったリモートプロシージャコール。

### 5-7. WebDAV
- WebDAVはHTTPを拡張することで分散ファイルシステムとして使えるようにしたもの

### 5-8. 共通の認証・認可プラットフォーム
- シングルサインオン
- Kerberos認証
- SAML
- OpenID
- OpenSosial
- OAuth
- OpenID Connect

- 認証(Authentication)
  - ログインしようとしてるユーザが「何者か？」を確認する。ブラウザを操作している人が、サービスに登録されているどのユーザIDの所有者なのかを確認する
  - 本人確認
- 認可(Authorization)
  - 認証したユーザが誰絵なのかを把握した上で、そのユーザに対してどこまでの権限を与えるかを決定する
  - 認めて許可すること
- フェデレーションログイン（ローカルログイン）
  - 自分のサービス以外が管理するIDを使ったログイン

## 7. HTTP2,HTTP3のシンタックス

### 7-2. HTTP/2

#### 7-2-2. 改善点
- ストリームを使ってバイナリデータを多重に送受信する仕組みに変更
- ストリーム内での優先順位設定や、サーバサイドからデータ通信を行うサーバサイドプッシュを実装
- ヘッダーば圧縮されるようになった

## 10. RESTful API
RESTfulの特性
- APIがウェブサーバを通じて提供されている
- GET /usr/[ユーザID]/repositories のように、パスに対してメソッドを送ることでサービスを得る
- APIの成功可否はステータスとしてクライアントに通知される
- URLはリソースの場所を表す表現であり、サービスの顔として大切である
- 必要に応じて、GETパラメータ、POSTのボディなどの追加情報を送信することもある
- サーバからの返り値としては、JSONやXMLのような構造化テキスト、あるいは画像データなどがかえってくることが多い

- URLはリソースの階層を表したパスになっている。名刺のみで構成される
- リソースに対して、HTTPメソッドを送ることでリソースの取得、更新、追加などの操作を行う
- ステータスを見ればリクエストが正しく処理されえたどうかが判定できる
- GETメソッドは何度読んでも状態を変更することがない
- クライアント側では管理すべきステータスが存在せず、1回ごとのリクエストは独立して発行できる
- トランザクションは存在しない

## 単語集
- RFCとは？
https://www.nic.ad.jp/ja/newsletter/No24/090.html
1. インターネット標準に関するもの
  - 標準化への提唱（PS:Proposed Standard）
  - 標準化への草稿（DS:Draft Standard）
  - 標準（STD: Standard）
2. その他
  - 情報（Info: Informational）
  - 実験（Exp: Experimental）
  - 歴史（Hist: Historical）
  - 現状（BCP: Best Current Practice）

- シンタックスとは？
  - プログラミング言語などの人工言語の仕様として定められた文法や表記法、構文規則などのルールを指す

- マッシュアップ
  - ウェブサービスを組み合わせて新しい付加価値を生み出す手法をマッシュアップと呼ぶ