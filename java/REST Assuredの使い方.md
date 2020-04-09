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



- JsonPathを使うと、取得したJsonをパースすることもできる
- POMに以下を追加

```xml
<dependency>
    <groupId>io.gatling</groupId>
    <artifactId>jsonpath_2.12</artifactId>
    <version>0.7.0</version>
</dependency>
```

- [Livedoorが提供しているWebAPI](http://weather.livedoor.com/weather_hacks/webservice)を使用して天気情報を取得する。
- 取得した情報の一部を表示する

```java
@Test
public void RestAssuredTest03() {
    RestAssured.baseURI = "http://weather.livedoor.com/forecast/webservice/json/v1";
    String response = given().param("city", "471010").get().asString();
    System.out.println(response);
    String city = JsonPath.from(response).get("location.city");
    System.out.println("city:"+city);
}
```

### 追記

- Jackson と 上で書いたJsonPathは一緒に使ったらまずいのかもしれないので、上記したパースするコードをJackconを使用したパターンで書き換え

```java
@Test
public void RestAssuredTest03() {
    RestAssured.baseURI = "http://weather.livedoor.com/forecast/webservice/json/v1";
    String response = given().param("city", "471010").get().asString();
    System.out.println(response);
    //以下Jackson使用したバージョン
    ObjectMapper mapper = new ObjectMapper();
    try {
        JsonNode node = mapper.readTree(response);
        String city = node.get("location").get("city").textValue();
        System.out.println("city:"+city);
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

