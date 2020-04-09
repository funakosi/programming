# REST Assured の使い方

## REST Assuredとは

REST Assured を使うと、REST APIのテストが簡単に行うことができる。

- 以下、参考にしたサイト
  - [公式ドキュメント](https://github.com/rest-assured/rest-assured/wiki)
  - [REST Assured を使ったREST API テスト](https://qiita.com/shimashima35/items/b85228d5bf5ec2708c5a)
  - [REST Assured を使ったREST API テスト その2](https://qiita.com/shimashima35/items/3e6edcdfb4e245922a58)



## REST Assuredの使い方

- POMに以下を追加

```xml
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>json-path</artifactId>
    <version>3.0.1</version>
</dependency>
```

- 以下のようなコードでテスト可能（これは上のサイト内の例をそのまま使用）

```Java
@Test
public void RestArruedTest01() {
    RestAssured.baseURI = "http://jsonplaceholder.typicode.com/";
    given()
        .get("/posts/2")
        .then()
        .body("userId", equalTo(1))
        .body("id", equalTo(2))
        .body("title", equalTo("qui est esse"));
}

@Test
public void RestArruedTest02() {
    RestAssured.baseURI = "http://jsonplaceholder.typicode.com/";
    given()
        .get("/posts/2")
        .prettyPrint(); //そのまま文字列としてコンソールに表示
}
```

