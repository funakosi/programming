# 実行可能なJARの作成

- テストコードも含め１つのJARに出来たら便利かな？と思って調べましたが、、結果からいうと良くわかっていません。Mainクラスは実行できてもテストクラスは含まれていなかったり、テスト用のjarは出力できても実行出来なかったり・・といった状態。
- MavenやExlipseといった開発環境に関する知識不足もあるので、ひとまず分かったことだけ共有



## Eclipseを使ってJAR化

- メニュー操作でjarを作成できるので、この方法が一番簡単か？
  - [実行可能JARの作り方と実行の仕方](https://www.ilovex.co.jp/blog/system/projectandsystemdevelopment/jar.html)ここらあたりを参考にすればすぐにできます。
  - 注意：Mavenでプロジェクト作成するとApp.javaが作成されるが、Main.javaに変更しておかないと（この名前のファイルがないと）メニューから選択できないらしい。

- ただし！このやり方だとテストコードが含まれないのでテストは実行できない



# MavenでJAR化

### Mainクラスのjar化

- これはうまくいったり、いかなかったりで良く分かっていません。
- [Mavenで実行可能なJARファイルを作成](https://yhayashi30.org/java/maven-create-jar-file/)このサイトで紹介されている方法でいけそう。このサイト内でGitHubプロジェクトの公開もされているので、git clone もしくは zipダウンロードで試すことは可能。
- ただし！このやり方もテストコードは含まれない（泣）



### テストクラスのjar化

- [テストコードと依存するライブラリをjarにまとめてCLIで実行する](https://qiita.com/halhide/items/e489d02f9622ce73b235)このサイトのやり方でできれば一番よかったが、少し古い情報なのでうまくいかず。（そもそもちゃんと理解していない可能性もあり）
- [How can I make the test jar include dependencies in Maven?](https://stackoverflow.com/questions/7000812/how-can-i-make-the-test-jar-include-dependencies-in-maven/11787964#11787964)このやり方だと Mainクラス用とテスト用のjarが2つできたが、関連するライブラリが含められなかったのと、実行ができなかった。



ということで手詰まりになったので、いったん塩漬け。

## 追記(2020/04/20)

- 一応 jar にした後にユニットテストを実行できる方法を見つけたので追記。ただし上記しているような考え方とは少し違い、Mainクラスの方でテストを実行するという考えで実装してみた。

- pom.xml の junitのスコープを削除
  - これをやらないと後々エラーとなる

【修正前】

```xml
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.11</version>
    <scope>test</scope>
</dependency>
```

【修正後】

```xml
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.11</version>
</dependency>
```

- selenideのサンプルを流用するのでpomに以下を追加しておく

```xml
<dependency>
    <groupId>com.codeborne</groupId>
    <artifactId>selenide</artifactId>
    <version>4.9.1</version>
</dependency>
```

- テストクラスを作成
  - ※src/main/java以下に作成

```java
package com.selenide.sample;

import static com.codeborne.selenide.Selenide.*;
import static org.hamcrest.CoreMatchers.*;
import static org.junit.Assert.*;
import java.util.logging.Logger;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import com.codeborne.selenide.Configuration;
import com.codeborne.selenide.WebDriverRunner;

public class SampleTest {
	private final static Logger log = Logger.getLogger(SampleTest.class.getName());
	@Before
	public void setUp() {
		Configuration.browser = WebDriverRunner.FIREFOX;
	    final String PATH = "exe/geckodriver.exe";
	    System.setProperty("webdriver.gecko.driver", PATH);
	}
	@Test
	public void test() {
		open("http://example.selenium.jp/reserveApp/");
		$("#reserve_day").val("22"); #※ここは当日日付以降の日を指定すること!
		$("#guestname").val("山田　太郎");
		$("#goto_next").click();
		$("#commit").click();
		assertThat($(By.tagName("h1")).getText(),is("予約を完了しました。"));
		sleep(2000);
		log.info("test01..pass");
	}
}
```

- Mainクラスでテストを呼び出す

```jara
package com.selenide.sample;

public class Main
{
    public static void main( String[] args )
    {
        SampleTest test = new SampleTest();
        test.test();
    }
}
```

- これでMainクラスを実行するとテストが実行される
- Eclipseから実行可能なjarを作成する
  - 以下では「sample.jar」という名前で作成したことを前提に説明している
- コマンドプロントから以下を実行することでテストが実行される

```
> >java -jar sample.jar
```

