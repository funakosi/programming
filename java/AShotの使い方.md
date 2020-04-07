# AShotの使い方

## AShotとは
- AShotを使用すればブラウザのするスクリーンショットを簡単に取得することができる
- 公式ドキュメントは[こちら](https://github.com/pazone/ashot)

## 使い方
1. POMファイルに以下を追加
    ```xml
    <dependency>
        <groupId>ru.yandex.qatools.ashot</groupId>
        <artifactId>ashot</artifactId>
        <version>1.5.2</version>
    </dependency>
    ```
2. Selnideを使用したサンプル
- 以下のコードを実行すると、プロジェクト直下に「screenshot.png」という画像が保存される。
- 注意）Windowsで実行する場合には、ディスプレイ設定の拡大率を100％にしておく必要あり。ここが125%や150%だと画像が見切れてしまう
```java
package com.selenide.sample;

import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import org.junit.Test;

import com.codeborne.selenide.Configuration;
import com.codeborne.selenide.Selenide;
import com.codeborne.selenide.WebDriverRunner;

import ru.yandex.qatools.ashot.AShot;
import ru.yandex.qatools.ashot.Screenshot;
import ru.yandex.qatools.ashot.shooting.ShootingStrategies;

public class SampleTest {
	@Test
	public void OpenSelenideSite() {
		 Configuration.browser = WebDriverRunner.FIREFOX;
	     final String PATH = "exe/geckodriver.exe";
	     System.setProperty("webdriver.gecko.driver", PATH);

	     Selenide.open("http://selenide.org");
	     Screenshot screenshot = new AShot()
	       .shootingStrategy(ShootingStrategies.viewportPasting(100))
	       .takeScreenshot(WebDriverRunner.getWebDriver());
	     try {
			ImageIO.write(screenshot.getImage(), "PNG", new File("screen.png"));
		} catch (IOException e) {
			e.printStackTrace();
		}

	     Selenide.sleep(2000);
	}
}

```
