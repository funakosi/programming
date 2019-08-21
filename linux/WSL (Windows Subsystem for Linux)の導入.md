# WSL (Windows Subsystem for Linux)の導入



## WSLとは

- WSL環境を構築すると、Windows10上でLinuxコマンドを実行できるようになる。

- [Microsoftが提供している資料](https://docs.microsoft.com/ja-jp/windows/wsl/about)



## WSLのインストール

- インストール方法はネット上に多く掲載されれている。
  - 「WSL　インストール」等のワードで検索すれば大量にヒットする
  - ここでは Ubuntuをインストールする
    - 2019年8月現在で３種類のUbuntuが存在するが、番号が何も記載されていないただの Ubuntuをインストールする



## WSLの使い方の基本

- Terminalの起動方法は、スタートメニューからUbuntuを起動することで可能
  他にも Windows のコマンドプロンプトで `bash` と打ち込むことで起動することもできる
- ホームディレクトリを変更する（[ここ](https://it-blue-collar-dairy.com/change_home_directory_for_ubuntu/)を参考）
  - ここではホームディレクトリを `C:\home` に変更するので、Cドライブの直下に `home`フォルダを作成しておく
  - Ubuntuのターミナルで、`$ sudo vim /etc/passwd` 
  - 自分のユーザ名の行の `/home/..`となっている個所を `/mnt/c/home` に変更する
  - 変更を反映するためにターミナルを閉じて再度立ち上げる
- その他の使い方等については、ネット上に多くの情報がある([こことか](https://qiita.com/rubytomato@github/items/fdfc0a76e848442f374e))ので各自検索して調べておくこと