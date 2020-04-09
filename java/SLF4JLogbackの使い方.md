# SLF4J/Logbackの使い方

## SLF4J/Logbackとは？

- SLF4JはJava用のシンプルなログファサード
  - [公式ドキュメント](http://www.slf4j.org/manual.html)

- Logback はJavaのロギングの実装
  - [公式ドキュメント](http://logback.qos.ch/manual/introduction_ja.html)



## 基本的な使い方

- [SLF4JとLogbackによるJavaのロギング入門](https://casualdevelopers.com/tech-tips/how-to-process-java-logging-with-slf4j-logback-lombok/)を参考に作成したコードの紹介。使い方等についてはリンク先を見ればわかると思う。

- POMの設定

```xml
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>1.7.25</version>
</dependency>
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
</dependency>
```

- src/main/resources に `logback.xml` を作成。内容は以下。

```xml
<configuration>
  <property name="encoding" value="UTF-8"/>
  <property name="logPath" value="logs/"/>
  <property name="logFormat" value="%date [%thread] [%-5level] %logger{40} = %message%n"/>

  <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
      <pattern>${logFormat}</pattern>
    </encoder>
  </appender>

  <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${logPath}app.log</file>

    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${logPath}app.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>30</maxHistory>
    </rollingPolicy>

    <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
      <charset>${encoding}</charset>
      <pattern>${logFormat}</pattern>
      <outputPatternAsHeader>true</outputPatternAsHeader>
    </encoder>
  </appender>

  <logger name="AppLog" level="TRACE"/>
  <logger name="TestLog" level="WARN"/>

  <root level="INFO">
    <appender-ref ref="STDOUT"/>
    <appender-ref ref="FILE"/>
  </root>
</configuration>
```

- App.java の内容は以下

```java
package com.selenide.sample;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class App
{
	private final static Logger log = LoggerFactory.getLogger("AppLog");

	public static void main( String[] args ){
		System.out.println("Hello World!\n");
        log.info("{} starting...", "My logging process");
        log.trace("Tracing...");
	    log.debug("Debugging...");
	    log.warn("Warning...");
	    log.error("Error handling...");
	    log.info("{} done.", "My logging process");
    }
}
```

- SampleTest#Logbacktest の内容は以下

```java
@Test
public void Logbacktest() {
    System.out.println("Hello World!\n");
    log.info("{} starting...", "My logging process");
    log.trace("Tracing...");
    log.debug("Debugging...");
    log.warn("Warning...");
    log.error("Error handling...");
    log.info("{} done.", "My logging process");
}
```

- mvn で実行してみる

```
>mvn exec:java -Dexec.mainClass="com.selenide.sample.App"
[INFO] Scanning for projects...
[INFO]
[INFO] ----------------< com.selenide.sample:selenide-sample >-----------------
[INFO] Building selenide-sample 1.0-SNAPSHOT
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] --- exec-maven-plugin:1.6.0:java (default-cli) @ selenide-sample ---

(省略)

Hello World!

2020-04-09 16:14:49,405 [com.selenide.sample.App.main()] [INFO ] AppLog = My logging process starting...
2020-04-09 16:14:49,410 [com.selenide.sample.App.main()] [TRACE] AppLog = Tracing...
2020-04-09 16:14:49,420 [com.selenide.sample.App.main()] [DEBUG] AppLog = Debugging...
2020-04-09 16:14:49,421 [com.selenide.sample.App.main()] [WARN ] AppLog = Warning...
2020-04-09 16:14:49,423 [com.selenide.sample.App.main()] [ERROR] AppLog = Error handling...
2020-04-09 16:14:49,433 [com.selenide.sample.App.main()] [INFO ] AppLog = My logging process done.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.522 s
[INFO] Finished at: 2020-04-09T16:14:49+09:00
[INFO] ------------------------------------------------------------------------
```

- projectフォルダ/logs/app.log の内容

```
#logback.classic pattern: %date [%thread] [%-5level] %logger{40} = %message%n
2020-04-09 16:14:49,405 [com.selenide.sample.App.main()] [INFO ] AppLog = My logging process starting...
2020-04-09 16:14:49,410 [com.selenide.sample.App.main()] [TRACE] AppLog = Tracing...
2020-04-09 16:14:49,420 [com.selenide.sample.App.main()] [DEBUG] AppLog = Debugging...
2020-04-09 16:14:49,421 [com.selenide.sample.App.main()] [WARN ] AppLog = Warning...
2020-04-09 16:14:49,423 [com.selenide.sample.App.main()] [ERROR] AppLog = Error handling...
2020-04-09 16:14:49,433 [com.selenide.sample.App.main()] [INFO ] AppLog = My logging process done.
```

- [Logback 使い方メモ]([https://qiita.com/opengl-8080/items/49719f2d35171f017aa9#%E3%83%AD%E3%82%AC%E3%83%BC%E3%81%AE%E5%87%BA%E5%8A%9B%E3%83%AC%E3%83%99%E3%83%AB%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%99%E3%82%8B](https://qiita.com/opengl-8080/items/49719f2d35171f017aa9#ロガーの出力レベルを指定する))に色々な使い方がまとめられているので、こちらも参考にする



## JSON形式でログを出力

- ログを後から分析する場合には、JSON形式のほうが何かと便利なので、出力形式をJSONとして吐き出せるか調査→できる
- 以下のサイトを参考にした
  - [LogstashのLogback JSON encoderで、Logbackで出力するログをJSONエンコードする](https://kazuhira-r.hatenablog.com/entry/2019/03/24/223923)
- POMに以下を追加

```xml
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>5.3</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-annotations</artifactId>
    <version>2.10.3</version>
</dependency>
```

- logback.xml の一部を変更

- 変更前

```xml
  <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${logPath}app.log</file>

    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${logPath}app.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>30</maxHistory>
    </rollingPolicy>

    <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
      <charset>${encoding}</charset>
      <pattern>${logFormat}</pattern>
      <outputPatternAsHeader>true</outputPatternAsHeader>
    </encoder>
  </appender>
```

- 変更後

```xml
<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${logPath}app.log</file>

    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${logPath}app.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>30</maxHistory>
    </rollingPolicy>
    <!-- ここを変更 -->
    <encoder class="net.logstash.logback.encoder.LogstashEncoder" />
  </appender>
```

- これで実行すると、コンソールに表示される文字は前回と同様だが、ファイルに出力されている内容がJSON形式となる

```json
{"@timestamp":"2020-04-09T16:24:01.578+09:00","@version":"1","message":"My logging process starting...","logger_name":"AppLog","thread_name":"main","level":"INFO","level_value":20000}
{"@timestamp":"2020-04-09T16:24:01.592+09:00","@version":"1","message":"Tracing...","logger_name":"AppLog","thread_name":"main","level":"TRACE","level_value":5000}
{"@timestamp":"2020-04-09T16:24:01.592+09:00","@version":"1","message":"Debugging...","logger_name":"AppLog","thread_name":"main","level":"DEBUG","level_value":10000}
{"@timestamp":"2020-04-09T16:24:01.592+09:00","@version":"1","message":"Warning...","logger_name":"AppLog","thread_name":"main","level":"WARN","level_value":30000}
{"@timestamp":"2020-04-09T16:24:01.592+09:00","@version":"1","message":"Error handling...","logger_name":"AppLog","thread_name":"main","level":"ERROR","level_value":40000}
{"@timestamp":"2020-04-09T16:24:01.592+09:00","@version":"1","message":"My logging process done.","logger_name":"AppLog","thread_name":"main","level":"INFO","level_value":20000}
```

- JSONを見やすく表示する`PrettyPrintingJsonGeneratorDecorator` や JSONに項目を追加する `MDC`の使い方は上記リンク内で詳しく説明されているので、そちらを参照