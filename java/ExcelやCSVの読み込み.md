# ExcelやCSVの読み込み

- タイトルの通り、データの読み込みをエクセルを使う方法とCSVを使う方法で試してみる



## 事前準備

- 使用するデータ

1. エクセル読み込みで使用するファイル　 [example.xlsx](data\example.xlsx) (196KB)（一部郵便番号データを使用）

2. CSV読み込みで使用するファイル　 [KEN_ALL.CSV](data\KEN_ALL.CSV) (18MB)（公開されている郵便番号のデータ）



## Excelを読み込む

- ここでは [XlsMapper](http://mygreen.github.io/xlsmapper/sphinx/index.html)を使用して読み込みを実施

- POMファイルの設定

```xml
<dependency>
    <groupId>com.github.mygreen</groupId>
    <artifactId>xlsmapper</artifactId>
    <version>2.1</version>
</dependency>
```

- 読み込むシートは以下（Listシート）
![list](./data\list.png)

- エクセルデータに対応するクラスを作成

```java
public enum Gender {
	male, female;
}
```

```java
public class UserRecord {
	@XlsColumn(columnName="ID")
    private int no;

    @XlsColumn(columnName="Class", merged=true)
    private String className;

    @XlsColumn(columnName="Name")
    private String name;

    @XlsColumn(columnName="Gender")
    private Gender gender;

	public int getNo() {
		return no;
	}

	public void setNo(int no) {
		this.no = no;
	}

	public String getClassName() {
		return className;
	}

	public void setClassName(String className) {
		this.className = className;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Gender getGender() {
		return gender;
	}

	public void setGender(Gender gender) {
		this.gender = gender;
	}

	@Override
	public String toString() {
		return "UserRecord [no=" + no + ", className=" + className + ", name=" + name + ", gender=" + gender + "]";
	}
}
```

```java
@XlsSheet(name="List")
public class UserSheet {

	@XlsLabelledCell(label="Date", type=LabelledCellType.Right)
	private Date createDate;

    @XlsHorizontalRecords(tableLabel="User List")
    private List<UserRecord> users;

	public Date getCreateDate() {
		return createDate;
	}

	public void setCreateDate(Date createDate) {
		this.createDate = createDate;
	}

	public List<UserRecord> getUsers() {
		return users;
	}

	public void setUsers(List<UserRecord> users) {
		this.users = users;
	}

	@Override
	public String toString() {
		return "UserSheet [createDate=" + createDate + ", users=" + users + "]";
	}
}
```

- 実際に読み込みを行う
  - 結果：２．５秒程度で読み込める（まぁまぁか）

```java
@Test
public void test01() {
    long startTime = System.currentTimeMillis();

    XlsMapper xlsMapper = new XlsMapper();
    try {
        UserSheet sheet = xlsMapper.
            load(new FileInputStream("example.xlsx"),UserSheet.class);
        System.out.println(sheet);
        long endTime = System.currentTimeMillis();
        System.out.println("処理時間：" + (endTime - startTime) + " ms");
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

- 次にもう少し大きめのシートを読み込む
  - これは愛媛の郵便番号の一覧（参考：1752行、15列、サイズ：196KB）

![zip38](./data\zip38.png)

- 前回と同様に読み込むためのクラスを作成して実際に読み込む

```java
@JsonPropertyOrder({
	"col01", "col02", "col03", "col04", "col05",
	"col06", "col07", "col08", "col09", "col10",
	"col11", "col12", "col13", "col14", "col15"})
public class Zip {
	private String col01;
	private String col02;
	private String col03;
	private String col04;
	private String col05;
	private String col06;
	private String col07;
	private String col08;
	private String col09;
	private String col10;
	private String col11;
	private String col12;
	private String col13;
	private String col14;
	private String col15;

	public Zip() {}

	public Zip(String col01, String col02, String col03, String col04, String col05,
               String col06, String col07, String col08, String col09, String col10,
               String col11, String col12, String col13, String col14,String col15) {
		super();
		this.col01 = col01;
		this.col02 = col02;
		this.col03 = col03;
		this.col04 = col04;
		this.col05 = col05;
		this.col06 = col06;
		this.col07 = col07;
		this.col08 = col08;
		this.col09 = col09;
		this.col10 = col10;
		this.col11 = col11;
		this.col12 = col12;
		this.col13 = col13;
		this.col14 = col14;
		this.col15 = col15;
	}

	public String getCol01() {
		return col01;
	}
	public void setCol01(String col01) {
		this.col01 = col01;
	}
	public String getCol02() {
		return col02;
	}
	public void setCol02(String col02) {
		this.col02 = col02;
	}
	public String getCol03() {
		return col03;
	}
	public void setCol03(String col03) {
		this.col03 = col03;
	}
	public String getCol04() {
		return col04;
	}
	public void setCol04(String col04) {
		this.col04 = col04;
	}
	public String getCol05() {
		return col05;
	}
	public void setCol05(String col05) {
		this.col05 = col05;
	}
	public String getCol06() {
		return col06;
	}
	public void setCol06(String col06) {
		this.col06 = col06;
	}
	public String getCol07() {
		return col07;
	}
	public void setCol07(String col07) {
		this.col07 = col07;
	}
	public String getCol08() {
		return col08;
	}
	public void setCol08(String col08) {
		this.col08 = col08;
	}
	public String getCol09() {
		return col09;
	}
	public void setCol09(String col09) {
		this.col09 = col09;
	}
	public String getCol10() {
		return col10;
	}
	public void setCol10(String col10) {
		this.col10 = col10;
	}
	public String getCol11() {
		return col11;
	}
	public void setCol11(String col11) {
		this.col11 = col11;
	}
	public String getCol12() {
		return col12;
	}
	public void setCol12(String col12) {
		this.col12 = col12;
	}
	public String getCol13() {
		return col13;
	}
	public void setCol13(String col13) {
		this.col13 = col13;
	}
	public String getCol14() {
		return col14;
	}
	public void setCol14(String col14) {
		this.col14 = col14;
	}
	public String getCol15() {
		return col15;
	}
	public void setCol15(String col15) {
		this.col15 = col15;
	}

	@Override
	public String toString() {
		return "Zip [col01=" + col01 + ", col02=" + col02 + ", col03=" + col03 + ",
            col04=" + col04 + ", col05=" + col05 + ", col06=" + col06 + ", 
            col07=" + col07 + ", col08=" + col08 + ", col09=" + col09 + ", 
            col10=" + col10 + ", col11=" + col11 + ", col12=" + col12 + ", 
            col13=" + col13 + ", col14=" + col14 + ", col15=" + col15 + "]";
	}
}
```

- 読み込み実施
  - 結果：133秒..2分以上かかるので実務で使うには少し厳しいかな？

```java
@Test
public void test03() {
    long startTime = System.currentTimeMillis();

    XlsMapper xlsMapper = new XlsMapper();
    try {
        ZipSheet sheet = xlsMapper.
            load(new FileInputStream("example.xlsx"),ZipSheet.class);
        System.out.println(sheet);
        long endTime = System.currentTimeMillis();
        System.out.println("処理時間：" + (endTime - startTime)/1000 + " s");
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```



# CSVを読み込む

- ここでは Jackson Dataformat CSVを使用して読み込む

- POMの設定

```xml
<dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-csv</artifactId>
    <version>2.10.3</version>
</dependency>
```

- 読み込むシートは全国の郵便番号データ！(12万行、18MB)

![image-20200414163635480](./data\zipall.png)

- クラスは上で掲載した ```Zip class```
- 読み込み用のコード
  - 結果：5秒程度.. やっぱプレーンテキスト強いかー。。

```java
@Test
public void test04() throws IOException {
    long startTime = System.currentTimeMillis();
    CsvMapper mapper = new CsvMapper();
    CsvSchema schema = mapper.schemaFor(Zip.class);

    Path path = Paths.get("KEN_ALL.CSV");
    try (BufferedReader br = Files.newBufferedReader(path)) {
        MappingIterator<Zip> it = mapper.readerFor(Zip.class).
            with(schema).readValues(br);
        while (it.hasNextValue()) { // 1行ずつ読み込む
            Zip csv = it.nextValue();
            System.out.println(csv);
        }
        long endTime = System.currentTimeMillis();
        System.out.println("処理時間：" + (endTime - startTime)/1000 + " s");
    }
}
```



