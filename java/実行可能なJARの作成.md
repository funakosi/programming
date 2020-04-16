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