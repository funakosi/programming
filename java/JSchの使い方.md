# JSchの使い方

## JSchとは

- Javaでリモートサーバにssh接続してシェルを実行できるライブラリ
- 他にsftpでファイルを送受信できる



## 準備

- ローカルサーバ環境を構築
  - [ローカル開発環境の構築 [Windows編]](https://dotinstall.com/lessons/basic_localdev_win_v2)を参考にしてローカルにCentOS環境を構築する
  - 上の通りに実行すると以下の設定値になる
    - IP: 192.168.33.10
    - port : 22
    - User: vagrant
    - Pass: vagrant

- 簡単なシェルを作成しておく

```bash
[vagrant@localhost ~]$ cat test.sh 
echo Hello World
exit 0
[vagrant@localhost ~]$ chmod +x test.sh 
[vagrant@localhost ~]$ ./test.sh 
Hello World
```



## シェルを実行し結果を取得する

- 以下のサンプルは「[リモートのサーバにSSH接続してコマンドを実行する](https://dev.classmethod.jp/articles/exec_remote_program/)」をベースに構築
- POMに追加

```xml
<dependency>
    <groupId>com.jcraft</groupId>
    <artifactId>jsch</artifactId>
    <version>0.1.55</version>
</dependency>
```

- クラスを作成

```java
import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.Closeable;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;

public class RemoteExecutor implements Closeable {

	private Session session;
	private ChannelExec channel;
	private String outputMessage;
	private String errMessage;

	/**
	 * Getter/Setter
	 */
	public String getOutputMessage() {
		return outputMessage;
	}

	public void setOutputMessage(String inputMessage) {
		this.outputMessage = inputMessage;
	}

	public String getErrMessage() {
		return errMessage;
	}

	public void setErrMessage(String errMessage) {
		this.errMessage = errMessage;
	}

	/**
	 * コンストラクタ
	 * @param host
	 * @param userName
	 * @param password
	 * @param port
	 * @throws Exception
	 */
	public RemoteExecutor (String host, String userName, String password, int port) {
		try {
			JSch jsch = new JSch();
			session = jsch.getSession(userName, host, port);
			session.setConfig("StrictHostKeyChecking", "no");
			session.setPassword(password);
			session.connect();
			channel = (ChannelExec)session.openChannel("exec");
		} catch (JSchException e) {
			// 例外時の処理
		}
	}

	/**
     * コマンドを実行する。
     * @param command
     * @return 処理結果
     * @throws IOException
     * @throws JSchException
     */
    public int execute(String command) throws Exception {
    	// コマンド実行する。
    	this.channel.setCommand(command);
    	channel.connect();
    	// 標準出力メッセージ
    	BufferedInputStream outStream = new BufferedInputStream(channel.getInputStream());
        ByteArrayOutputStream bout = new ByteArrayOutputStream();
        byte[] buf = new byte[1024];
        int length;
        while (true) {
            length = outStream.read(buf);
            if (length == -1) {
                break;
            }
            bout.write(buf, 0, length);
        }
        outputMessage = new String(bout.toByteArray(), StandardCharsets.UTF_8);
    	// エラーメッセージ用Stream
        BufferedInputStream errStream = new BufferedInputStream(channel.getErrStream());
        bout = new ByteArrayOutputStream();
        buf = new byte[1024];
        while (true) {
            int len = errStream.read(buf);
            if (len <= 0) {
                break;
            }
            bout.write(buf, 0, len);
        }
        // エラーメッセージ取得する
        errMessage = new String(bout.toByteArray(), StandardCharsets.UTF_8);
        channel.disconnect();
        // コマンドの戻り値を取得する
        int returnCode = channel.getExitStatus();
        return  returnCode;
    }

    @Override
	public void close() {
		session.disconnect();
	}
}
```

- ローカル環境のシェルを実行するサンプル

```java
@Test
public void sshTest01() {
    try (RemoteExecutor executor = new RemoteExecutor("192.168.33.10", "vagrant", "vagrant", 22)) {
        int returnCode = executor.execute("/home/vagrant/test.sh");
        System.out.println("status:"+returnCode);
        System.out.println(executor.getOutputMessage());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

- 実行結果は以下のようになる

```
status:0
Hello World
```

