Amazon Linux2でローカル環境構築

## 概要

- Amazon Linux2を扱うにあたり、手元にも同様の環境があったほうがいいと思うので、その構築方法を検討。ネット上にある情報を参考に、Vagrantで構築した方法を説明



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





**## インストール**



\- 適当なフォルダ作成

 \- vagrant init bento/amazonlinux-2

 \- ファイルのIP箇所のコメントを外し、IPを適当に変更

\- `vagrant up`

\- https://app.vagrantup.com/bento/boxes/amazonlinux-2 

\- https://techblog.recochoku.jp/5048



**## デスクトップ環境構築**

\- https://urashita.com/archives/31409

\- 上のサイトの内容を実行する

 \- vns-pass:password



**## seleniumお試しは以下とフォントインストール,Chromeインストールも以下**

\- https://qiita.com/onorioriori/items/371d2cc790f9d7bec505

\- 日本語化はされているのでFONTSの設定は不要

\- Webドライバはバージョンを確認してDLすること





**## java/jdk**

\- udo yum install -y java-1.8.0-openjdk

\- sudo yum install -y java-1.8.0-openjdk-devel



**## maven**

\- https://weblabo.oscasierra.net/install-maven-35-centos7/

\- →この手順でいける



**## git**

\- yum install git