Amazon Linux2でローカル環境構築

## 概要

- Amazon Linux2（以降 AM2と表記）を扱うにあたり、手元にも同様の環境があったほうがいいと思うので、その構築方法を検討。ネット上にある情報を参考に、Vagrantで構築した方法を説明



## 必要となるソフト

- Virtual Box
- Vagrant

上の２つは事前にインストールしておく事。またインストールする順は、Virtual Box->Vagrantでないと後々面倒なことになる。



## Amazon Linux2インストール

- 適当なフォルダを作成
  `> mkdir amazonlinux2`
- 以下のコマンドで初期化
  `vagrant init bento/amazonlinux-2`
- 作成される`Vagrantfile`を編集
  - config.vm.network の箇所をコメント解除

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/amazonlinux-2"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP. ※以下をコメント解除、IPはお好みで変更する
  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end

```

- 以下のコマンドでインストール実行（時間がかかるので少し待つ）
  `vagrant up`

- 参考URL
  - https://app.vagrantup.com/bento/boxes/amazonlinux-2 
  -  https://techblog.recochoku.jp/5048

- インストール後の確認
  - vagrant status
    OSが起動中かどうか確認
  - vagrant ssh
    OSにSSH接続
  - vagrant halt
    OSをシャットダウン
- PuttyやRLogin等でSSH接続を試す
  - IP Address
    - 上の設定ファイルの通りであれば、192.168.33.10
  - User/Pass
    - いずれも vagrant



## デスクトップ環境の構築

このままでも開発は出来るが、やっぱりデスクトップ環境があったほうが便利なので導入してみる。色々調べたが今分かっているのは、Mateをインストールし、VNCで接続するという手順。以降の手順は、[Amazon Linux2にGUIデスクトップ環境をインストールする手順](https://urashita.com/archives/31409)というサイトの流れにそっています。

### MATEのインストール

- まずはパッケージを最新にする
  `$ sudo yum update`
- AM2にMATEをインストール

```bash
#MATEパッケージをインストール
$ sudo amazon-linux-extras install mate-desktop1.x
#MATEをデフォルトのデスクトップとして定義
$ sudo bash -c 'echo PREFERRED=/usr/bin/mate-session > /etc/sysconfig/desktop'
#VNCサーバの導入
$ sudo yum install tigervnc-server
#VNCのパスワード設定
 #->ここでは password とした
$ vncpasswd
Password: <パスワードを入力>
Verify: <パスワードを入力>
Would you like to enter a view-only password (y/n)? n
A view-only password is not used
#VNCサーバを１度起動
$ vncserver :1
#新しいsystemdユニット作成
$ sudo cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@.service
#※以下の手順は上のリンク先と違います。ユーザはec2-userではなくvagrant!
#<USER>をvagrantに書き換え
$ sudo sed -i 's/<USER>/vagrant/' /etc/systemd/system/vncserver@.service
#systemdマネージャ設定をリロード
$ sudo systemctl daemon-reload
#VNCサービスを有効にする
$ sudo systemctl enable vncserver@:1
#VNCサービスを起動
$ sudo systemctl start vncserver@:1
```

- WindowsにTightVNCクライアントをインストール
  - https://www.tightvnc.com/download.php
  - 上からインストーラを入手しインストール（細かい手順は省略）
- TIghtVNC Viewerを起動する
  ここまでの手順通りに設定していれば、`192.168.33.10:5901`で接続できる
  - Vnc Authenticationダイアログに入力する値は`vncpasswd`で設定したもの。ここでは `password`
  - これで画面を表示される

### MATEの日本語化

日本語化を実施。以降の流れも[Amazon Linux2にGUIデスクトップ環境をインストールする手順](https://urashita.com/archives/31409)というサイトの説明にそっています。

```bash
# IME ibus/google-noto-sans-japanese-fontsをインストール
$ sudo yum install ibus-kkc
$ sudo yum install google-noto-sans-japanese-fonts
# ibusの設定
$ vi ~/.bashrc
# 以下を末尾に追加
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
ibus-daemon -drx
# ロケールを変更
$ sudo localectl set-locale LANG=ja_JP.UTF-8
# リブート
$ sudo reboot
```

OS再起動後に再度 TightVNCで接続すると、日本語になっていることがわかる。



## その他

- デフォルトだと画面サイズが小さいので適当なサイズに変更する
  - VNCで接続後に、システム＞設定＞ディスプレイ＞解像度で設定する



## Seleniumを試す

今構築したAmazon Linux2環境にSelenium環境を構築してみる。ここからの手順は、[Amazon Linux2でSelenium環境を最短で構築する](https://qiita.com/onorioriori/items/371d2cc790f9d7bec505)で紹介されている流れに即している。

- Google Chromeのインストール

```bash
# Google Chromeをインストール
$ curl https://intoli.com/install-google-chrome.sh | bash
# バージョン確認
$ google-chrome --version
Google Chrome 83.0.4103.97
```

- GConf2のインストール

```bash
$ yum -y install GConf2
```

- Chrome Driverのインストール
  - 以下のURLからChromeのバージョンに適合するドライバーを取得
    https://chromedriver.chromium.org/downloads
  - 以降は、Version8.3の場合

```bash
$ wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ mv chromedriver /usr/local/bin/
```

- Google Noto Fontsのインストール
  →日本語表示用のフォントは既にインストール済なので、この手順は不要

- Seleniumのインストール

```bash
# pipのインストール
$ sudo yum install -y python-pip
# seleniumのインストール
$ sudo pip install selenium
```

- PythonでSeleniumを試す
  以下のソースも[Amazon Linux2でSelenium環境を最短で構築する](https://qiita.com/onorioriori/items/371d2cc790f9d7bec505)で紹介されているもの

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,1024')
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.google.co.jp/')
driver.save_screenshot('test.png')
```

`python test.py` でフォルダ内にtest.pngが作成されていれば成功。

`options.add_argument('--headless')`をコメントアウトして、VNC環境で実行すると実際にブラウザが起動するのが分かる。

## Java環境構築

- Java/JDKのインストール
  以下のコマンドでjava 環境を構築

```bash
$ sudo yum install -y java-1.8.0-openjdk
$ sudo yum install -y java-1.8.0-openjdk-devel

# 確認
$ java -version
openjdk version "1.8.0_252"
OpenJDK Runtime Environment (build 1.8.0_252-b09)
OpenJDK 64-Bit Server VM (build 25.252-b09, mixed mode)
$ javac -version
javac 1.8.0_252
```



- mavenのインストール
  - 以下のリンクの手順でインストールを実行
    https://weblabo.oscasierra.net/install-maven-35-centos7/
  - 以下の手順でエラーになる場合は、sudo 等を試す

```bash
# download
$ curl -OL https://archive.apache.org/dist/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz
# /optフォルダに配置
$ tar -xzvf apache-maven-3.5.2-bin.tar.gz
$ mv apache-maven-3.5.2 /opt/
# リンク作成
$ cd /opt
$ ln -s /opt/apache-maven-3.5.2 apache-maven

# パスを追加
vim ~/.bash_profile
# 以下を末尾に追加
JAVA_HOME=/usr/java/default/
PATH=$PATH:/opt/apache-maven/bin
# 再読み込み
$ source ~/.bash_profile

# 確認
$ mvn -versoin
Apache Maven 3.5.2 (138edd61fd100ec658bfa2d307c43b76940a5d7d; 2017-10-18T07:58:13Z)
Maven home: /opt/apache-maven
Java version: 1.8.0_252, vendor: Oracle Corporation
Java home: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.252.b09-2.amzn2.0.1.x86_64/jre
Default locale: ja_JP, platform encoding: UTF-8
OS name: "linux", version: "4.14.181-140.257.amzn2.x86_64", arch: "amd64", family: "unix"
```

- gitのインストール

```bash
$ sudo yum install git
```



- VSCodeのインストール

[AmazonLinux2にVisual Studio Codeインストール](https://qiita.com/rururu_kenken/items/b04471b580fab126bea4)の手順にそってVSCodeをインストール

```bash
# 鍵とリポジトリ登録
$ sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
$ sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'

# VSCodeのインストール
$ sudo yum -y install code
# 確認
$ code -version
code -version
Warning: 'e' is not in the list of known options, but still passed to Electron/Chromium.
Warning: 'i' is not in the list of known options, but still passed to Electron/Chromium.
Warning: 'o' is not in the list of known options, but still passed to Electron/Chromium.
1.46.0
a5d1cc28bb5da32ec67e86cc50f84c67cc690321
x64
```

これでVNCで接続時にVSCodeがGUI環境で使えるようになる。ここでは説明を省くが、ここまでの流れで以下のようなことが可能になる（はず）。

- git clone でソース取得
- mvn clean compile test でテスト
- VSCodeのjava開発環境プラグインをインストール
  - git clone で取得したソースを開き、VSCode上で開発等々

