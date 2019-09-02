# Selenium入門ドリル用環境構築

テスト自動化研究会のサイトで公開されている`Selenium入門ドリル`を行うための環境構築手順を記載していく。



## 前提条件

- JDKとEclipseをインストール後にGitから学習用コードを取得する
  （JDKのインストールとパスの設定は必須作業ではない可能性有）
- 教材はテスト自動化研究会のサイト内にある「[４時間で学ぶ、効率的な自動テストスクリプトのメンテナンス](https://sites.google.com/site/testautomationresearch/teaching_materials/maintainable_script)」を参照。また同じページ内にある「前提知識・事前準備手順ドキュメント」も参照。



## 1. JDKのインストール

- Oracleのサイトから最新版のJDKをダウンロードする
  - 詳細は「[Java環境構築(Windows版) JDKインストール](https://techfun.cc/java/windows-jdk-install.html)」を参照
  - Oracleのダウンロードサイトは [こちら](https://www.oracle.com/technetwork/java/javase/downloads/index.html)
    - 32bit/64bitに注意してダウンロード
- インストールを実行する



## 2. パスの設定

- JDKをインストール後に、環境変数の設定とパスの設定を行う
  - 詳細は「[Java環境構築(Windows版) パスの設定](https://techfun.cc/java/windows-jdk-pathset.html)」を参照
    - JAVA_HOMEの設定
    - JAVA_HOME\bin へパスを通す



## 3. Eclipseのインストール

- 現時点での最新版をダウンロードする
  - 詳細は「[Java環境構築(Windows版) Eclipseのインストール](https://techfun.cc/java/windows-eclipse-install.html)」を参照
  - ここでは上の記載と同じ「Eclipse 4.8 Photon」を使用した



## 4. gitからソースを取得

- 学習用コードは「[STARHOTEL-Teaching-Materials](https://github.com/SoftwareTestAutomationResearch/STARHOTEL-Teaching-Materials)」から取得可能
  - Clone か Zipでダウンロードし使用する

- ダウンロード後、Eclipseを起動
  以下の手順は、「[４時間で学ぶ、効率的な自動テストスクリプトのメンテナンス](https://sites.google.com/site/testautomationresearch/teaching_materials/maintainable_script)」のサイト内にある「前提知識・事前準備手順ドキュメント」に含まれている
  1. ファイル > インポート
  2. 既存のプロジェクトをワークスペースへ を選択し、次へボタンを押す
  3. ルートディレクトリを選択の参照ボタンから、上でダウンロードしたディレクトリを選択し完了ボタンを押す
- WebDriverを自分の環境にあったものに変更する



## 5. 環境が正常に設定されているかチェック

- インポートされた「STARHOTEL-Teaching-Materials」の test-(デフォルトパッケージ)-EnvironmentCheck.javaを開く
- EnvironmentCheck.javaを右クリックし、実行＞JUnitテストを選択
- インストールや設定が正しく行われていれば、テストは成功する



※うまくいかない場合のチェックポイント

- JDKがインストールされているか？
- JAVA_HOMEが設定されパスが通っているか？
- Eclipseの設定が正常に実行されているか？
- WebDriverが自分の環境にあったものか？



## 6. Selenium入門ドリルを元に学習する

- 「[４時間で学ぶ、効率的な自動テストスクリプトのメンテナンス](https://sites.google.com/site/testautomationresearch/teaching_materials/maintainable_script)」の１スライド目から順に処理を追っておく。スライドの概要は以下の通り

1. Seleniumの基本的な使い方
   1. 入門課題
   2. 実践課題
2. Seleniumテストを効率よく実施する方法
   1. ページオブジェクトデザインパターン
   2. サイトが変更されたときの対応方法

- このドリルは自動化テストを対象としているが、この内容を理解していけばプログラムの基礎（共通関数化とかクラス化）の概念も理解できる。また他自動化ツールの操作方法にも応用できる箇所が多々あるので、何度も繰り返し学習することを勧める
- 最初は写経（答えをただコピーしていくだけの作業）でもいい。２回、３回と繰り返すことで基本が身についていくはずである



## この後は？

- 今回作成したテストケースと同じ内容を別のプログラム言語やライブラリ等を使用して実装してみる
  - 同じ言語の場合：Javaの Selenide、Geb
  - 別言語の場合：PythonやRuby
  - 別ツール：Appium 等
- テスト対象のサイトを拡張してみる
  - テスト対象のサイトを改良し動的にページが変化するようなものにしテスト実施を試す
  - 例えば登録した予約内容をCSVやDBに登録し一覧画面で表示させてみる等々

