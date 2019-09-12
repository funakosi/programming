# Seleniumとは

Seleniumとは何か？を色々なリソースをもとに説明。

このサイトではこう言っている、あの書籍ではこういう表現をしているという説明。



## 本家Seleniumサイト（英語）

### Seleniumとは?

[本家サイト](https://www.seleniumhq.org/)の説明

```
What is Selenium?
Selenium automates browsers. That's it! What you do with that power is entirely up to you. Primarily, it is for automating web applications for testing purposes, but is certainly not limited to just that. Boring web-based administration tasks can (and should!) be automated as well.

Selenium has the support of some of the largest browser vendors who have taken (or are taking) steps to make Selenium a native part of their browser. It is also the core technology in countless other browser automation tools, APIs and frameworks.
```

- Seleniumはブラウザをオートメーション化する。

- Seleniumはブラウザベンダーからのサポートを受けている
  - （各種ブラウザに対応するWebDriverはベンダーがメンテナンスする）ことを言っているのだと思う

### WebDriverとかBrowserDriverとかの話

主に本家サイトの「[このページ](https://www.seleniumhq.org/download/)」や「[SeleniumやらWebDriverやら](https://qiita.com/memodasu/items/f06c65513272c1ba7948)」から引用

- ものすごく雑に説明すると以下のようになる
  Seleniumが各言語用に準備したライブラリから各種ブラウザ用のドライバを経由してブラウザを操作する
  - Seleniumが準備したライブラリ→各種ブラウザのドライバ→ブラウザ
- ここでSeleniumが準備したライブラリというのが、上の本家サイトの「[このページ](https://www.seleniumhq.org/download/)」内にある `Selenium Client & WebDriver Language BIndings`の項目
- さらに各種ブラウザ用に準備されているドライバ（これをWebDriverといったりBrowserDriverと言ったりする）が、同じく本家サイトのページ内にある `Third Party Drivers, Bindings, and Plugins`の項目
- ただしIEだけはSelenim側が独自でサポートとしているらしく、上の項目にはなく変わりに `The Internet Explorer Driver Server`という項目から取得できる



## SeleniumHQサイト（日本語）

[Seleniumのコミュニティサイト](http://oss.infoscience.co.jp/seleniumhq/docs/01_introducing_selenium.html)の説明。ただし更新日を見ると大分古い。

```
Selenium は、Web ベースアプリケーションのテスト自動化の高速開発をサポートした堅牢なツール群です。Selenium は、Web アプリケーションのテストニーズに特化したテスト機能を豊富に備えています。テスト操作の柔軟性は高く、UI 要素を特定したり、テストの期待値と実際のアプリケーションの動作を比較したりするための多数のオプションを利用できます。

1 つのテストを多数のブラウザプラットフォームで実行できる点は、Selenium の優れた特徴のひとつです。
```

[Seleniumのコンポーネント](http://oss.infoscience.co.jp/seleniumhq/index.html)

- Selenium IDE
  - FireFoxアドオン、マウスやキーボード操作でテスト作成可能
  - 内部実装は古い
- Selenium Remote Control (RC)
  - 作成されたテストを各種ブラウザとプラットフォームで実行可能
- Selenium Grid
  - Selenium RCを拡張して、複数のサーバにテストを分散できる

## SeleniumとWebDriverの最新事情

CodeZineの[記事](https://codezine.jp/article/detail/10225)で、このサイトに書かれている内容は「エキスパートが教えるSelenium最前線」に記載されている内容とほぼ同じ。以下は[そのサイトの記事](https://codezine.jp/article/detail/10225)の抜粋。

### Seleniumの変遷

- （Selenium1->Selenium2->Selenium3）



![Selenium1 â Selenium2 â Selenium3](https://cz-cdn.shoeisha.jp/static/images/article/10225/102205_01.gif)



### 最近の大きな変化

- W3CによるWebDriverの標準規格化（標準化されつつある）



![W3Cå§åã¾ã§ã®ãã­ã»ã¹](https://cz-cdn.shoeisha.jp/static/images/article/10225/102205_02.gif)

- Appiumの適用範囲の拡大
- 有用な拡張・支援ソフトの普及
  - Java/Java互換：Selenide, Geb
  - Ruby：Capybara