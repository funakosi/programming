# Cucumberの使い方

- Cucumberとは？（[こちら](https://www.infoq.com/jp/news/2018/06/cucumber-bdd-ten-years/)のサイトより抜粋）

> Cucumberは、TDD(テスト駆動開発)の一種であるBDDをサポートするツールです。BDDでは、テストは*すべて*ユーザによる受け入れテストです。技術者でないステークホルダでも理解可能なように、平易な(人の)言語で記述されます。Cucumberでは、要求仕様と自動テストと“生きたドキュメント”を、Gherkinという、平易な英語と簡易な構造を持ったひとつのフォーマットにまとめています。

- ここでは、[Selenium with Cucumber (BDD Framework): Tutorial with Example](Selenium with Cucumber (BDD Framework): Tutorial with Example)で説明されている内容をベースに解説していく
- ちなみに Cucumberはキュウリという意味で発音はカタカナで書くとキューカンバー。



## 準備

- 基本的な環境については、[ここ](https://github.com/funakosi/programming/tree/master/selenium)を参照
  - JDK, Maven, Eclipse, FireFoxのインストールと設定を終わらせておく
- Eclipseのプラグインをインストールしておく
  - ヘルプ＞マーケットプレイス＞Cucumberで検索しインストール



## Cucumberを使ってテスト作成

- ここではまずCucumberを使った簡単なサンプルを作成する
- 次にSelenideを使ったUIテストを実施後にパラメータ化テストを実装する

- 簡単な手順を記載

1. プロジェクト作成
   - pomへの記載
2. 簡単なサンプルを追加
3. Selenideを使ったUIテストを追加
4. UIテストをパラメータ化テストに変更



## 1. プロジェクト作成

```
> mvn archetype:generate -DgroupId=com.example.sample -DartifactId=CucumberSample
> cd CucumberSample
> mvn eclipse:eclipse
```

- Eclipseで今作成したプロジェクトをインポート
- pomへ追加

```xml
<!-- コンパイラを1.8に変更 -->
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
</properties>
<!-- Cucumber関連とSelenideを追加 -->
<dependencies>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.11</version>
        <scope>test</scope>
    </dependency>
    <!-- https://mvnrepository.com/artifact/io.cucumber/cucumber-java -->
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-java</artifactId>
        <version>5.6.0</version>
    </dependency>
    <!-- https://mvnrepository.com/artifact/io.cucumber/cucumber-junit -->
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-junit</artifactId>
        <version>5.6.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>com.codeborne</groupId>
        <artifactId>selenide</artifactId>
        <version>4.9.1</version>
    </dependency>
</dependencies>
```



## 2. 簡単なサンプルを追加

- プロジェクト直下にFeaturesとう名前のフォルダを作成し、そこにMyTest.featureという名前のファイルを作成。プラグインが正常にインストールされていれば、以下のように自動でコードが入力される

![image-20200429113652422](./data/cucumber00)

- コメントは削除し以下のようにコードを変更する
  - これがテストシナリオとなる

```gherkin
@サンプル
Feature: サンプルテスト
  文字列を出力するだけのサンプル

  @テスト
  Scenario: サンプル
    Given FireFoxを開きアプリを起動する
	When ユーザ名とパスワードを入力
    Then 資格情報をリセット
```

- 次に上のシナリオに対応するコードを記載する
- steps という名前のパッケージを追加し、そのパッケージ内に SampleSteps.javaを追加

- SampleSteps.javaの中身は以下

```java
package com.example.sample.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

public class SampleSteps {
	@Given("^FireFoxを開きアプリを起動する$")
    public void open_the_Firefox_and_launch_the_application() throws Throwable
    {
        System.out.println("Open the Firefox and launch the application.");
    }

	@When("^ユーザ名とパスワードを入力$")
    public void enter_the_Username_and_Password() throws Throwable
    {
    	System.out.println("Enter the Username and Password.");
    }

    @Then("^資格情報をリセット$")
    public void Reset_the_credential() throws Throwable
    {
        System.out.println("Click on the Reset button.");
    }
}
```

- テストを実行するためのエントリポイントを作成する

- runnersという名前のパッケージを作成し、そこにSampleRunner.javaを追加
- SampleRunner.javaのコードは以下

```java
package com.example.sample.runners;

import org.junit.runner.RunWith;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
		features="Features", //featureファイルのある場所
		glue={"com.example.sample.steps"}, //featureに対応するコードがある場所
		strict=true //これ書かないと警告が表示される
)
public class SampleRunner {

}
```

- ここまでの作業で以下のようなフォルダ構成となっている

![image-20200429115444189](./data/cucumber01)

- SampleRunnerを実行すると、コンソールに以下のように表示されテストが成功となる。

```
Open the Firefox and launch the application.
Enter the Username and Password.
Click on the Reset button.

1 Scenarios ([32m1 passed[0m)
3 Steps ([32m3 passed[0m)
0m0.558s
```



## 3. Selenideを使ったUIテストを追加

- 2.で作ったサンプルを改良してUIテストを実施できるようにする
- プロジェクト直下に driver という名前のフォルダを作成し、そこにfirefox用のwebdriverをコピーする
- こんな感じ

![image-20200429120858884](./data/cucumber02)

- SampleRunner.javaを修正

```java
package com.example.sample.runners;

import org.junit.BeforeClass;
import org.junit.runner.RunWith;

import com.codeborne.selenide.Configuration;
import com.codeborne.selenide.WebDriverRunner;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
		features="Features",
		glue={"com.example.sample.steps"},
		strict=true
)
public class SampleRunner {
	@BeforeClass
    public static void setUp(){
        Configuration.browser = WebDriverRunner.FIREFOX;
        System.setProperty("webdriver.chrome.driver", "driver/geckodriver.exe");
    }
}
```

- SampleSteps.javaを修正

```java
package com.example.sample.steps;

import org.openqa.selenium.By;

import com.codeborne.selenide.Selenide;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

public class SampleSteps {
	@Given("^FireFoxを開きアプリを起動する$")
    public void open_the_Firefox_and_launch_the_application() throws Throwable
    {
        System.out.println("Open the Firefox and launch the application.");
        Selenide.open("http://demo.guru99.com/v4");
    }

	@When("^ユーザ名とパスワードを入力$")
    public void enter_the_Username_and_Password() throws Throwable
    {
    	System.out.println("Enter the Username and Password.");
    	 Selenide.$(By.name("uid")).val("username12");
         Selenide.$(By.name("password")).val("password12");
    }

    @Then("^資格情報をリセット$")
    public void Reset_the_credential() throws Throwable
    {
        System.out.println("Click on the Reset button.");
        Selenide.$(By.name("btnReset")).click();
    }
}
```

- これで先ほどと同じようにテストを実行すると、FireFoxが起動しテストが実行される

## 4. UIテストをパラメータ化テストに変更

- 最後に上で作成したUIテストをパラメータテストに変更する

- MyFeature.featureを修正
  - **Scenario Outline**になっているので注意

```gherkin
@サンプル
Feature: サンプルテスト
  文字列を出力するだけのサンプル

  @テスト
  Scenario Outline: サンプル
    Given FireFoxを開きアプリを起動する
    When ユーザ名 <username> とパスワード <password> を入力
    Then 資格情報をリセット

Examples:
|username  |password         |
|User1     |password1        |
|User2     |password2        |
|User3     |password3        |

```

- SampleSteps.javaを修正

```java
package com.example.sample.steps;

import org.openqa.selenium.By;

import com.codeborne.selenide.Selenide;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

public class SampleSteps {
	@Given("^FireFoxを開きアプリを起動する$")
    public void open_the_Firefox_and_launch_the_application() throws Throwable
    {
        System.out.println("Open the Firefox and launch the application.");
        Selenide.open("http://demo.guru99.com/v4");
    }

	@When("^ユーザ名 (.+) とパスワード (.+) を入力$")
    public void enter_the_Username_and_Password(String username,String password) 
        throws Throwable
    {
    	System.out.println("Enter the Username and Password on the login page.");
        Selenide.$(By.name("uid")).val(username);
        Selenide.$(By.name("password")).val(password);
    }

    @Then("^資格情報をリセット$")
    public void Reset_the_credential() throws Throwable
    {
        System.out.println("Click on the Reset button.");
        Selenide.$(By.name("btnReset")).click();
    }
}
```

- これでテスト実行すると、Examplesで提示されている資格情報をパラメータとしテストを実施する

### ちなみに..

- SampleRunner.javaを以下のように変更するとログの表示が変更し、さらにテスト実行後「{Project}\target\cucumber-html-report」にレポートが出力される。なかなか便利。

![image-20200429123028541](./data/cucumber03)

- ソースコードはGitHubのレポジトリにあげています。
  - https://github.com/funakosi/CucumberSample



## 参考にしたサイト

- [Selenium with Cucumber (BDD Framework): Tutorial with Example](Selenium with Cucumber (BDD Framework): Tutorial with Example)

- [GUIテストの自動化と結果の可視化](GUIテストの自動化と結果の可視化)
- [Selenium と Cucumber を使用した自動テスト](https://www.ibm.com/developerworks/jp/agile/library/a-automating-ria/index.html)

- [Cucumber Reference](https://cucumber.io/docs/cucumber/api/)