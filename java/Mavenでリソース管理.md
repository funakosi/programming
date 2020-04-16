# Mavenでリソース管理

- Mavenでプロジェクト管理する場合、どうやってリソース持つのがいいのか？を検証
- まずMavenでのデフォルトは以下のようになっているらしい
  - 通常実行：src/main/resources
  - テスト実行：src/test/resources
  - [Mavenのresourcesフォルダについて整理してみた](https://qiita.com/tontan9616/items/d8427504e82c68be3b03)が分かりやすいです
- 別のフォルダをリソースフォルダとしたい場合には以下を参照
  - [Mavenのリソースフォルダの場所を変更する](https://www.codeflow.site/ja/article/maven__how-to-change-maven-resources-folder-location)
- Mavenプロジェクトの場合、基本的には src/main/resources を使い、テストでのみ使うリソースを src/test/resources で管理するという風にすればよさそう



## リソースの読み込み

- リソースの読み取りには、`getClass().getResourceAsStream("/<filename>")`を使用する

- [Java - リソースフォルダからファイルを読み込む](https://www.codeflow.site/ja/article/java__java-read-a-file-from-resources-folder)のサイトを参照

### 実験

- 同じ名前のファイルを main/resources と test/resources以下に配置し、通常実行とテスト実行でどうなるか調べる

```
> type src/main/resources/file.txt
src/main/resources/file.txt
Hello
本日は晴天なり！
> type src/test/resources/file.txt
src/test/resources/file.txt
Hello
本日は晴天なり！
```

- Main.java でテスト

```java
public class Main {

	  public static void main(String[] args) {
		  Main obj = new Main();
		  System.out.println(obj.getFile("file.txt"));
	  }

	  private String getFile(String fileName) {
	      StringBuilder result = new StringBuilder("");
	      //Get file from resources folder
	      ClassLoader classLoader = getClass().getClassLoader();
	      File file = new File(
              classLoader.getResource(fileName).getFile());

	      try (Scanner scanner = new Scanner(file)) {
	          while (scanner.hasNextLine()) {
	              String line = scanner.nextLine();
	              result.append(line).append("\n");
	          }
	          scanner.close();
	      } catch (IOException e) {
	    	  e.printStackTrace();
	      }
	      return result.toString();
	  }
}
```

- 結果はsrc/main/resources/file.txtが表示される

- 次にテストコードで試す

```java
public class ResourceTest {

	@Test
	public void testHello() {

	      String result = getFile("file.txt");
	      System.out.println(result);

	}

	private String getFile(String fileName) {
	    StringBuilder result = new StringBuilder("");
	   //Get file from resources folder
	    ClassLoader classLoader = getClass().getClassLoader();
	    File file = new File(
            classLoader.getResource(fileName).getFile());

	    try (Scanner scanner = new Scanner(file)) {
	        while (scanner.hasNextLine()) {
	            String line = scanner.nextLine();
	            result.append(line).append("\n");
	        }
	        scanner.close();
	    } catch (IOException e) {
	        e.printStackTrace();
	    }
	    return result.toString();
	  }

```

- 結果はsrc/test/resources/file.txtが表示される
- 試しに test/resources/file.txt を file2.txt に変更して実行
  - すると src/main/java/file.txt が表示される



## その他

- 開発や本番環境でリソースを入れ替えたい場合などにはプロファイルを使えばいいらしい
  - [Maven2で環境に合わせて設定ファイルを切り替える方法（改訂版）](http://trinityt.hatenablog.jp/entry/20080516/1210908204)