# 		HTTP通信

- 色々な方法でHTTP通信を行う



## 準備

- Git for Windows のインストール
  - [公式サイト](https://gitforwindows.org/)からインストーラを入手しインストール
- jq のインストール
  - [公式サイト](https://stedolan.github.io/jq/)からダウンロードし保存した場所にパスを通す



## 一覧化

- この資料で説明する方法と使用するサイトの一覧を示す

| No   | 手法                   | Livedoor api   | httpbin       |                | JSONPlaceholder |              |
| ---- | ---------------------- | -------------- | ------------- | -------------- | --------------- | ------------ |
|      |                        | GET            | GET           | POST           | GET             | POST         |
| 1    | curl                   | 1-livedoor-get | 1-httpbin-get | 1-httpbin-post | 1-place-get     | 1-place-post |
| 2    | java HttpURLConnection | 2-livedoor-get | 2-httpbin-get | 2-httpbin-post | 2-place-get     | 2-place-post |
| 3    | java Rest Assured      | 3-livedoor-get | 3-httpbin-get | 3-httpbin-post | 3-place-get     | 3-place-post |
| 4    | java OkHttp            | 4-livedoor-get | 4-httpbin-get | 4-httpbin-post | 4-place-get     | 4-place-post |

- 通信手段の説明

1. curl コマンドでデータを取得する方法を説明
2. Java 標準であるHttpURLConnectionを使用してデータを取得する方法を説明
3. Java のRest Assuredを使ってデータを取得する方法を説明
4. Java のOkHttpを使ってデータを取得する方法を説明

- 使用するサイトの説明

1. livedoor api

   お天気情報を取得できる[サイト](http://weather.livedoor.com/weather_hacks/webservice)

2. httpbin

   シンプルなHTTPリクエストとレスポンスを返してくれるサービス

3. JSONPlaceholder

   RESTで実装されたAPIサーバーです。ダミーデータを返却してくれる



## 1. CURL

### 1-livedoor-get

Livedoorの天気情報をCURLで取得

- 都市名を取得
```bash
> curl -X GET http://weather.livedoor.com/forecast/webservice/json/v1?city=471010 | jq -r ".location.city"
```
- 進捗を省略
```
> curl -X GET -s http://weather.livedoor.com/forecast/webservice/json/v1?city=471010 | jq -r ".location.city"
```



### 1-httpbin-get

- httpbin にパラメータ「a=1, b=2」を付与してリクエスト
```> curl -X GET -s "http://httpbin.org/get?a=1&b=2"```
- パラメータ「a」を確認
```> curl -X GET -s "http://httpbin.org/get?a=1&b=2" | jq -r ".args.a"```



### 1-httpbin-post

- POST form
```> curl -X POST  -d "param1=aa&param2=bb" http://httpbin.org/post | jq -r ".form"```
- POST json/data
```
> curl -X POST  -H "Content-Type: application/json" -d '{"param1":"aa","param2":"bb"}' http://httpbin.org/post | jq -r ".data"
```
- POST json/data args
```> curl -X POST  -d "param1=aa&param2=bb" "http://httpbin.org/post?a=1&b=2"```

### 1-place-get

```> curl -X GET -s "https://jsonplaceholder.typicode.com/posts/1" | jq -r ".id"```

### 1-place-post

```
> curl -X POST  -H "Content-Type: application/json; charset=UTF-8" -d '{"title":"a1 test","body":"this is test by a1.","userId":1}' https://jsonplaceholder.typicode.com/posts/  | jq -r ".title"
```



## 2. java HttpURLConnection

- [HttpURLConnectionを使ってPOSTやGETでリクエストするサンプル(proxyも考慮)](https://web.plus-idea.net/2016/08/httpurlconnection-post-get-proxy-sample/)のサイトに記載されているコードを参考に（ほぼそのまま）クラスを作成

```java
/**
 * refer from below site
 *https://web.plus-idea.net/2016/08/httpurlconnection-post-get-proxy-sample/
 */
public class MyUtil {
	private static Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("xxxxxxxx.co.jp", 8080));
    private static String proxySwitch = "0";


    public static String callGet(String strGetUrl){

        HttpURLConnection con = null;
        StringBuffer result = new StringBuffer();

        try {

            URL url = new URL(strGetUrl);

            if(proxySwitch.equals("1")){
                con = (HttpURLConnection) url.openConnection(proxy);
            }else{
                con = (HttpURLConnection) url.openConnection();
            }

            con.setRequestMethod("GET");
            con.connect();

            // HTTPレスポンスコード
            final int status = con.getResponseCode();
            if (status == HttpURLConnection.HTTP_OK) {
                // 通信に成功した
                // テキストを取得する
                final InputStream in = con.getInputStream();
                String encoding = con.getContentEncoding();
                if(null == encoding){
                    encoding = "UTF-8";
                }
                final InputStreamReader inReader = new InputStreamReader(in, encoding);
                final BufferedReader bufReader = new BufferedReader(inReader);
                String line = null;
                // 1行ずつテキストを読み込む
                while((line = bufReader.readLine()) != null) {
                    result.append(line);
                }
                bufReader.close();
                inReader.close();
                in.close();
            }else{
                System.out.println(status);
            }

        }catch (Exception e1) {
            e1.printStackTrace();
        } finally {
            if (con != null) {
                // コネクションを切断
                con.disconnect();
            }
        }
        System.out.println("result=" + result.toString());
        return result.toString();
    }


    public static String callPost(String strPostUrl, String strContentType, String formParam){

        HttpURLConnection con = null;
        StringBuffer result = new StringBuffer();

        try {
            URL url = new URL(strPostUrl);

            if(proxySwitch.equals("1")){
                con = (HttpURLConnection) url.openConnection(proxy);
            }else{
                con = (HttpURLConnection) url.openConnection();
            }

            con.setDoOutput(true);
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", strContentType);
            OutputStreamWriter out = new OutputStreamWriter(con.getOutputStream());
            out.write(formParam);
            out.close();
            con.connect();

            // HTTPレスポンスコード
            final int status = con.getResponseCode();
            if (status == HttpURLConnection.HTTP_OK ||
            	status == HttpURLConnection.HTTP_CREATED) {
                // 通信に成功した
                // テキストを取得する
                final InputStream in = con.getInputStream();
                String encoding = con.getContentEncoding();
                if(null == encoding){
                    encoding = "UTF-8";
                }
                final InputStreamReader inReader = new InputStreamReader(in, encoding);
                final BufferedReader bufReader = new BufferedReader(inReader);
                String line = null;
                // 1行ずつテキストを読み込む
                while((line = bufReader.readLine()) != null) {
                    result.append(line);
                }
                bufReader.close();
                inReader.close();
                in.close();
            }else{
                System.out.println(status);
            }

        }catch (Exception e1) {
            e1.printStackTrace();
        } finally {
            if (con != null) {
                // コネクションを切断
                con.disconnect();
            }
        }
        System.out.println("result=" + result.toString());
        return result.toString();
    }
}
```

- 上のクラスを使用して、リストに記載されている組み合わせを試す

```java
public class HttpNativeSample {

	/**
	 * MyUtil: https://web.plus-idea.net/2016/08/httpurlconnection-post-get-proxy-sample/
	 * Json=>Pojo: http://www.jsonschema2pojo.org/
	 * @throws IOException
	 */
	@Test
	public void LivedoorGetSample() throws IOException {
		String result = MyUtil.callGet("http://weather.livedoor.com/forecast/webservice/json/v1?city=471010");
		ObjectMapper mapper = new ObjectMapper();
		JsonNode node = mapper.readTree(result);
		String city = node.get("location").get("city").textValue();
		System.out.println("city:"+city);
	}

	@Test
	public void HttpbinGetSample() throws IOException {
		String result = MyUtil.callGet("http://httpbin.org/get?a=1&b=2");
		ObjectMapper mapper = new ObjectMapper();
		JsonNode node = mapper.readTree(result);
		System.out.println("args:"+node.get("args").toString());
	}

	@Test
	public void HttpbinPostSample() throws IOException {
		ObjectMapper mapper = new ObjectMapper();
		//POST form
		String result = MyUtil.callPost("http://httpbin.org/post", "application/x-www-form-urlencoded", "param1=aa&param2=bb");
		JsonNode node = mapper.readTree(result);
		System.out.println("form:"+node.get("form").toString());
		//POST json/data
		result = MyUtil.callPost("http://httpbin.org/post", "application/json", "param1=aa&param2=bb");
		node = mapper.readTree(result);
		System.out.println("data:"+node.get("data").toString());
		//POST json/data args
		result = MyUtil.callPost("http://httpbin.org/post?a=1&b=2", "application/json", "param1=aa&param2=bb");
		node = mapper.readTree(result);
		System.out.println("args:"+node.get("args").toString());
		System.out.println("data:"+node.get("data").toString());
	}

	@Test
	public void JsonPlaceholderGetSample() throws IOException {
		String result = MyUtil.callGet("https://jsonplaceholder.typicode.com/posts/1");
		ObjectMapper mapper = new ObjectMapper();
		JsonNode node = mapper.readTree(result);
		System.out.println("title:"+node.get("title").toString());
	}

	@Test
	public void JsonPlaceholderPostSample() throws IOException {
		String json = "{\"title\":\"a1 test\",\"body\":\"this is test by a1.\",\"userId\":1}";
		String result = MyUtil.callPost("https://jsonplaceholder.typicode.com/posts/","application/json",json);
		ObjectMapper mapper = new ObjectMapper();
		JsonNode node = mapper.readTree(result);
		System.out.println("title:"+node.get("title").toString());
	}
}
```



## 3. java Rest Assured

- POMに以下を追加

```xml
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <version>4.3.0</version>
</dependency>
```

- リストに記載されている組み合わせを試す

```java
public class RestAssuredSample {

	private final static Logger log = LoggerFactory.getLogger("TestLog");

	@Test
	public void LivedoorGetSample() {
		try {
			RestAssured.baseURI = "http://weather.livedoor.com/forecast/webservice/json/v1";
	        given()
	        	.param("city", "471010")
	            .get("")
	        .then()
	        	.statusCode(200)
	        	.body("location.city", equalTo("那覇"));
	        log.info("success");
		} catch (AssertionError e) {
			log.error(e.getLocalizedMessage());
		}
	}

	@Test
	public void HttpbinGetSample() {
		RestAssured.baseURI = "http://httpbin.org/get";
        given()
        	.param("a", "1")
        	.param("b", "2")
            .get("")
        .then()
        	.statusCode(200)
        	.body("args.a", equalTo("1"))
        	.body("args.b", equalTo("2"));
	}

	@Test
	public void HttpbinPostSample01() {
		RestAssured.baseURI = "http://httpbin.org/post";
        given()
        	.param("param1", "aa")
        	.param("param2", "bb")
            .post("")
        .then()
        	.statusCode(200)
        	.body("form.param1", equalTo("aa"))
        	.body("form.param2", equalTo("bb"));
	}

	@Test
	public void HttpbinPostSample02() {
		RestAssured.baseURI = "http://httpbin.org/post";
		String json = "{\"param1\":\"aa\",\"param2\":\"bb\"}";
        given()
        	.header("Content-Type", "application/json")
        	.body(json)
            .post("")
        .then()
        	.statusCode(200)
        	.body("json.param1", equalTo("aa"))
        	.body("json.param2", equalTo("bb"));
	}

	@Test
	public void JsonPlaceholderGetSample() throws IOException {
		RestAssured.baseURI = "https://jsonplaceholder.typicode.com/posts/1";
        given()
        	.get("")
        .then()
        	.statusCode(200)
        	.body("userId", equalTo(1));
	}

	@Test
	public void JsonPlaceholderPostSample() throws IOException {
		RestAssured.baseURI = "https://jsonplaceholder.typicode.com/posts/";
		String json = "{\"title\":\"a1 test\",\"body\":\"this is test by a1.\",\"userId\":1}";
        given()
        	.header("Content-Type", "application/json")
        	.body(json)
        	.post("")
        .then()
        	.statusCode(201)
        	.body("title", equalTo("a1 test"));
	}

}
```

- 他と比べると大分すっきりかける！



## 4. java OkHttp

- POMに以下を追加

```xml
<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>4.5.0</version>
</dependency>
```

- リストに記載されている組み合わせを試す

```java
public class OkHttpSample {

	@Test
	public void LivedoorGetSample() throws IOException {
		String BASE_URL = "http://weather.livedoor.com/forecast/webservice/json/v1";
		HttpUrl.Builder urlBuilder
	      = HttpUrl.parse(BASE_URL).newBuilder();
	    urlBuilder.addQueryParameter("city", "471010");

	    Request request = new Request.Builder()
	  	      .url(urlBuilder.build().toString())
	  	      .build();

        OkHttpClient client = new OkHttpClient();
        Response response = client.newCall(request).execute();

        ObjectMapper mapper = new ObjectMapper();
		JsonNode node = mapper.readTree(response.body().string());
		String city = node.get("location").get("city").textValue();
		System.out.println("city:"+city);
	}

	@Test
	public void HttpbinGetSample() throws IOException {
		String BASE_URL = "http://httpbin.org/get";
		HttpUrl.Builder urlBuilder = HttpUrl.parse(BASE_URL).newBuilder();
	    urlBuilder.addQueryParameter("a", "1");
	    urlBuilder.addQueryParameter("b", "2");

	    Request request = new Request.Builder()
	  	      .url(urlBuilder.build().toString())
	  	      .build();

        OkHttpClient client = new OkHttpClient();
        Response response = client.newCall(request).execute();
        String body = response.body().string();
        System.out.println(body);

        ObjectMapper mapper = new ObjectMapper();
        JsonNode node = mapper.readTree(body);
		String args = node.get("args").toString();
		System.out.println("args:"+args);
	}

	@Test
	public void HttpbinPostSample01() throws IOException {
		String BASE_URL = "http://httpbin.org/post";
		HttpUrl.Builder urlBuilder = HttpUrl.parse(BASE_URL).newBuilder();

		MediaType mediaTypeJson = MediaType.get("application/json; charset=utf-8");
		OkHttpClient client = new OkHttpClient();
		String json = "{\"param1\":\"aa\",\"param2\":\"bb\"}";
		RequestBody requestBody = RequestBody.create(mediaTypeJson, json);
		Map<String, String> httpHeaders = new LinkedHashMap<String, String>();
		Request request = new Request.Builder()
                .url(urlBuilder.build().toString())
                .headers(Headers.of(httpHeaders))
                .post(requestBody)
                .build();
		Response response = client.newCall(request).execute();
        String resultStr = response.body().string();
        System.out.println(resultStr);
	}

	@Test
	public void JsonPlaceholderGetSample() throws IOException {
		Request request = new Request.Builder()
                .url("https://jsonplaceholder.typicode.com/posts/1")
                .get()
                .build();

        OkHttpClient client = new OkHttpClient();

        Response response = client.newCall(request).execute();
        System.out.println(response.body().string());
	}

	@Test
	public void JsonPlaceholderPostSample() throws IOException {
		String BASE_URL = "https://jsonplaceholder.typicode.com/posts/";
		HttpUrl.Builder urlBuilder = HttpUrl.parse(BASE_URL).newBuilder();

		MediaType mediaTypeJson = MediaType.get("application/json; charset=utf-8");
		OkHttpClient client = new OkHttpClient();
		String json = "{\"title\":\"a1 test\",\"body\":\"this is test by a1.\",\"userId\":1}";
		RequestBody requestBody = RequestBody.create(mediaTypeJson, json);
		Map<String, String> httpHeaders = new LinkedHashMap<String, String>();
		Request request = new Request.Builder()
                .url(urlBuilder.build().toString())
                .headers(Headers.of(httpHeaders))
                .post(requestBody)
                .build();
		Response response = client.newCall(request).execute();
        String resultStr = response.body().string();
        System.out.println(resultStr);
	}

}
```

- Rest Assured に比べるとコードが少し分かりにくいか？