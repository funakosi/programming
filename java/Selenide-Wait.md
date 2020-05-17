# Selenide-Wait

SelenideでWaitを使う方法を説明。具体的なサンプルサイトをもとに説明するほうがいいが、適当なものが見当たらなかったので、参考になるサイトとSeleniumのサンプルサイトを用いて説明する。



## 参考にしたサイト

- [Selenideを活用したい人に向けて](https://qiita.com/motoki1990/items/abe3b7472097d7e6085f)
- [Java実装のWebDriverラッパー Selenideを使う](https://qiita.com/shimashima35/items/a437f0ed080a9ba71b72)
- [Selenide公式ドキュメント](https://selenide.org/documentation.html)

[番外辺]

- [Guru99](http://demo.guru99.com/test/login.html) このサイトのAjaxが使えるかと思ったけどダメだった



## SelenideのWait

まずはWaitの使い方を公式ドキュメントから把握。２つあるようだ。

- waitUntil(Condition, milliseconds)
- waitWhile(Condition, milliseconds)

上のいずれかを使用して、Conditionを適切に記述できれば待ってくれる。

ということでConditionの使い方を公式から把握するために該当箇所だけ抜き取り。

```
com.codeborne.selenide.Condition [src] [javadoc]
Conditions are used in should / shouldNot / waitUntil / waitWhile constructs. We recommend to import corresponding conditions statically to receive all the advantages of readable code:

visible / appear // e.g. $(“input”).shouldBe(visible)
present / exist // // conditions to wait for element existence in DOM (it can be still hidden)
hidden / disappear // not(visible)
readonly // e.g. $(“input”).shouldBe(readonly)
name // e.g. $(“input”).shouldHave(name(“fname”))
value // e.g. $(“input”).shouldHave(value(“John”))
type // e.g. $(“#input”).shouldHave(type(“checkbox”))
id // e.g. $(“#input”).shouldHave(id(“myForm”))
empty // e.g. $(“h2”).shouldBe(empty)
attribute(name) // e.g. $(“#input”).shouldHave(attribute(“required”))
attribute(name, value) // e.g. $(“#list li”).shouldHave(attribute(“class”, “active checked”))
cssClass(String) // e.g. $(“#list li”).shouldHave(cssClass(“checked”))
focused
enabled
disabled
selected
matchText(String regex)
text(String substring)
exactText(String wholeText)
textCaseSensitive(String substring)
exactTextCaseSensitive(String wholeText)
Look for more details in Selenide gitbook
```

参考サイトにある例を列挙。(https://qiita.com/motoki1990/items/abe3b7472097d7e6085f)

```java
Selenide.$("#tablecaption").waitWhile(Condition.exactValue(preTableCation), 5);
```

https://qiita.com/shimashima35/items/a437f0ed080a9ba71b72

```java
$("#submit").waitUntil(enable, 1000).click()
```

- Seleniumサンプルサイトを使用したサンプルを提示
  - 別にWait入れなくても動作しているけど。。

```java
public class SampleTest {

	private final static Logger log = Logger.getLogger(SampleTest.class.getName());

	@Before
	public void setUp() {
		Configuration.browser = WebDriverRunner.FIREFOX;
	    final String PATH = "exe/geckodriver.exe";
	    System.setProperty("webdriver.gecko.driver", PATH);
	}

	@Test
	public void testselenide() {
		open("http://example.selenium.jp/reserveApp/");
		LocalDate nextDay = DateTools.getNextDay(
            $("#reserve_year").val(),
            $("#reserve_month").val(),
            $("#reserve_day").val());
		$("#reserve_day").val(String.valueOf(nextDay.getDayOfMonth()));
		$("#guestname").val("山田　太郎");
		$("#goto_next").click();
		$("#commit").waitUntil(Condition.enabled, 3000).click();
		assertThat($(By.tagName("h1")).getText(),is("予約を完了しました。"));
		sleep(2000);
		log.info("test01..pass");
	}
}
```

上のソース内で使われている DatTools#getNextDday のソースは以下。翌日以降でないと次の画面に移行できないので、こういう仕組みにしています。

```java
public class DateTools {
	public static LocalDate getNextDay(String year, String month, String day) {
		LocalDate date =
				LocalDate.of(
						Integer.valueOf(year),
						Integer.valueOf(month),
						Integer.valueOf(day));
		return date.plusDays(1);
	}
}
```

