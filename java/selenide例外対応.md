# Selenideの例外対応

要素取得等で例外が起きた場合の対処方法を検討



## Javaにおける一般的な例外の対応方法

- 例外クラスの継承関係
  - 参考：新わかりやすいJavaオブジェクト指向徹底解説
  - 参照：[【Java】例外の種類と基本的な処理](https://qiita.com/shg3/items/f5d12ec1088d18ac7702)

- Throwable
  - Exception
    - RuntimeException **(2)**
      - ArithmeticException
      - NullPointerException
      - IndexOutOfBoundsExeption
      - ClassCastException
      - IllegalArgumentException ...etc
    - IOException
    - SQLException
    - ReflectiveOperationExeption ...etc
  - Error **(1)**
    - OutOfMemoryError
    - ClassFormatError ...etc

(1) システムエラー：プログラムで例外処理はしない

(2) 実行時例外（非チェック例外）：例外処理は必須ではない

(3) チェック例外  上記一覧の (1) と (2) 以外：必ずtryを使用して例外処理を行う



### まとめ

| 種類           | 例外作成     | 対応           |
| -------------- | ------------ | -------------- |
| システムエラー | JVM          | 何もしない     |
| チェック例外   | メソッド     | 例外処理が必須 |
| 実行時例外     | JVM,メソッド | 任意           |



## Selenideで例外処理

- selenideを使用してテスト実施時の例外対応を検証

- Seleniumの[テストサイト](http://example.selenium.jp/reserveApp/)を使用して簡単なサンプルを作成する

```java
public class SelenideSample {

	@Before
	public void setUp() {
		Configuration.browser = WebDriverRunner.FIREFOX;
	    final String PATH = "exe/geckodriver.exe";
	    System.setProperty("webdriver.gecko.driver", PATH);
	}

	@Test
	public void test01() {
		open("http://example.selenium.jp/reserveApp/");
		$("#reserve_day").val("15");
		$("#guestname").val("山田　太郎");
		$("#goto_next").click();
		$("#commit").click();
		assertThat($(By.tagName("h1")).getText(),is("予約を完了しました。"));
		sleep(2000);
	}
}
```

このコードを1か所だけ変更しエラーとなるようにする。タイプミスしたと改定して、以下のように変更

```java
$("#goto_next").click(); -> $("#goto_nex").click();
```

実行すると期待通りエラーとはなる。次にテストの経緯をログに吐き出してみることを考える。

```java
package com.selenide.sample;

import static com.codeborne.selenide.Selenide.*;
import static org.hamcrest.CoreMatchers.*;
import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.codeborne.selenide.Configuration;
import com.codeborne.selenide.WebDriverRunner;
import com.codeborne.selenide.ex.ElementNotFound;

public class SelenideSample {

	//slf4j使用
	private final static Logger log = LoggerFactory.getLogger("TestLog");

	@Before
	public void setUp() {
		Configuration.browser = WebDriverRunner.FIREFOX;
	    final String PATH = "exe/geckodriver.exe";
	    System.setProperty("webdriver.gecko.driver", PATH);
	}

	@Test
	public void test01() {
		try {
			open("http://example.selenium.jp/reserveApp/");
			$("#reserve_day").val("15");
			$("#guestname").val("山田　太郎");
			$("#goto_nex").click();
			$("#commit").click();
			assertThat($(By.tagName("h1")).getText(),is("予約を完了しました。"));
			sleep(2000);
			log.info("test01..pass");
		} catch (ElementNotFound e) {
			log.error("test01..failed");
			log.error(e.getLocalizedMessage());
		}
	}
}
```

- 実行すると以下のようなエラーが出たが、JUnit的にはパスしてしまった。

```
2020-04-14 11:58:05,344 [main] [ERROR] TestLog = test01..failed
2020-04-14 11:58:05,347 [main] [ERROR] TestLog = Element not found {#goto_nex}
Expected: visible
```

- catch の中で１行追加して解決

```java
@Test
public void test01() {
    try {
        open("http://example.selenium.jp/reserveApp/");
        $("#reserve_day").val("15");
        $("#guestname").val("山田　太郎");
        $("#goto_nex").click();
        $("#commit").click();
        assertThat($(By.tagName("h1")).getText(),is("予約を完了しました。"));
        sleep(2000);
        log.info("test01..pass");
    } catch (ElementNotFound e) {
        log.error("test01..failed");
        log.error(e.getLocalizedMessage());
        fail(e.getMessage()); //追加
    }
}
```

- さて、一番最初に書いた一般的な例だとシステムエラーは例外処理をする必要とないとあるが、ElementNotFoundの親をたどっていくと以下のようになっておりErrorのサブクラスであることが分かる。上の話だとこれは例外処理を必要としないが、、この場合はしょうがないのか？それとも別の手段があるのか今後もう少し検討が必要か？

- Error
  - AssertionError
    - UIAssertionError
      - ElementNotFound