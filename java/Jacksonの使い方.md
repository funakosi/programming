# Jacksonの使い方

## Jacksonとは

- JSONをJavaのオブジェクトに変換したり、その逆を行ったりすることを手軽に実装できるライブラリ



## Jacksonの使い方

- pom.xml に以下を追加
  - バージョン等最新の情報については、[こちらのサイト](https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-core)を参照

```xml
<!-- https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-core -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.10.3</version>
</dependency>
```

- 以降のサンプルは、[こちらの記事](https://qiita.com/opengl-8080/items/b613b9b3bc5d796c840c)の通りにすることで簡単に確認できるので省略