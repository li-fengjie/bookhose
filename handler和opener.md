## Handler处理器 和 自定义Opener

```python
opener是 urllib2.OpenerDirector 的实例，我们之前一直都在使用的urlopen，它是一个特殊的opener（也就是模块帮我们构建好的）。
	（1）前面学习的urllib.request.urlopen()很简单的一个获取网页的函数，但是它不能自己构建请求头
	（2）引入了request对象，request = urllib.request.Request(url=url, headers=headers),它的高级之处就是可以自己定制请求头
	（3）request对象不能携带cookie，也不能使用代理，所以引入了Handler处理器、自定义Opener

但是基本的urlopen()方法不支持代理、cookie等其他的HTTP/HTTPS高级功能。所以要支持这些功能：
1、使用相关的Handler处理器来创建特定功能的处理器对象；
2、然后通过urllib2.build_opener()方法使用这些处理器对象，创建自定义opener对象；
3、使用自定义的opener对象，调用open()方法发送请求。

如果程序里所有的请求都使用自定义的opener，可以使用urllib2.install_opener()将自定义的 opener 对象 定义为 全局opener，表示如果之后凡是调用urlopen，都将使用这个opener（根据自己的需求来选择）

```

### 简单的自定义opener()
```python
import urllib
from urllib import request

# 构建一个HTTPHandler 处理器对象，支持处理HTTP请求
handler = urllib.request.HTTPHandler()  # http

# 构建一个HTTPHandler 处理器对象，支持处理HTTPS请求
# handlers = urllib.request.HTTPSHandler()  # 处理https的处理器

# 调用urllib2.build_opener()方法，创建支持处理HTTP请求的opener对象
opener = urllib.request.build_opener(handler)

# 构建 Request请求
req = urllib.request.Request("http://www.baidu.com", headers=headers)

# 调用自定义opener对象的open()方法，发送request请求
response = opener.open(req)

# 获取服务器响应内容
print(response.read())




```
```python
import urllib
from urllib import request

# 特殊的打开器opener
# urllib.request.urlopen()

# 自定义打开器: 主要用于cookie,代理
# 创建处理器对象
http = urllib.request.HTTPHandler()  # http处理器
# debuglevel=1 : 会在控制台输出日志信息
# http = urllib.request.HTTPHandler(debuglevel=1)  # http处理器,
# https = urllib.request.HTTPSHandler()  # https处理器

# 创建打开器对象
opener = urllib.request.build_opener(http)

# 设置为全局打开器
# 那么后面的urlopen也会使用全局打开器对象
urllib.request.install_opener(opener)

# 打开url
response = opener.open("http://www.baidu.com/")
print(response)
print(response.read().decode())

# urlopen
# response = urllib.request.urlopen("http://www.ifeng.com/")
# print(response)


```



这种方式发送请求得到的结果，和使用urllib2.urlopen()发送HTTP/HTTPS请求得到的结果是一样的。

```python
如果在 HTTPHandler()增加 debuglevel=1参数，还会将 Debug Log 打开，这样程序在执行的时候，会把收包和发包的报头在屏幕上自动打印出来，方便调试，有时可以省去抓包的工作

# 仅需要修改的代码部分：

# 构建一个HTTPHandler 处理器对象，支持处理HTTP请求，同时开启Debug Log，debuglevel 值默认 0
http_handler = urllib2.HTTPHandler(debuglevel=1)

# 构建一个HTTPSHandler 处理器对象，支持处理HTTPS请求，同时开启Debug Log，debuglevel 值默认 0
https_handler = urllib2.HTTPSHandler(debuglevel=1)
```

#### Cookie案例：

##### 1.获取Cookie

```python
import urllib.request
from http import cookiejar  # python3
# import cookiejar  # python2

# 创建一个对象存储cookie
cookies = cookiejar.LWPCookieJar()
# cookie处理器, 提取cookie
cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
# 创建打开器, 处理cookie
opener = urllib.request.build_opener(cookie_handler)

# 使用opener打开url
response = opener.open("http://www.baidu.com/")
# 得到cookies
print(cookies)

```
2. ##### 下载cookie
```python
import urllib.request
from http import cookiejar

filename = "baiducookie.txt"  # 用于保存cookie
# 管理cookie的对象
cookies = cookiejar.LWPCookieJar(filename=filename)
# 创建cookie处理器
cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
# 创建打开器
opener = urllib.request.build_opener(cookie_handler)

# 添加UA，并打开百度，下载cookie
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

req = urllib.request.Request("http://www.baidu.com", headers=headers)

# 打开
response = opener.open(req)

# 保存， 忽略错误
cookies.save(ignore_discard=True, ignore_expires=True)

```
3. ##### 使用下载的cookie
```python
import urllib.request
from http import cookiejar

filename = "baiducookie.txt"
cookies = cookiejar.LWPCookieJar()

# 使用cookie
cookies.load(filename)

cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
opener = urllib.request.build_opener(cookie_handler)

# 添加UA，并打开百度
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

req = urllib.request.Request("http://www.baidu.com", headers=headers)
response = opener.open(req)

```

##### 示例： cookie登录qq空间

```python
1，用自己的账号登录qq空间，将登录成功后的cookie拷贝出来
2，将拷贝出来的cookie保存在HTTP头部信息headers中
3，使用headers发送请求
QQ空间： https://user.qzone.qq.com/904552498
```

##### 练习： 登录人人网

```python
# 人人网登录接口： 
url = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2018921035604"
# 参数：
data = {
    "email": "18566218481",
    "icode": "",
    "origURL": "http://www.renren.com/home",
    "domain": "renren.com",
    "key_id": "1",
    "captcha_type": "web_login",
    "password": "1260ec8f79d73201e2e7aaca932e88465dffe9f59bd7104a9d7c1bac981dad59",
    "rkey": "44fd96c219c593f3c9612360c80310a3",
    "f": "http%3A%2F%2Fwww.renren.com%2F548819077%2Fprofile",
}

1， 保存登录成功后的cookie
2， 使用保存的cookie进行登录， 登录后获取个人信息
	url = "http://www.renren.com/548819077/profile"

```

### ProxyHandler处理器（代理设置）

```python
使用代理IP，这是爬虫/反爬虫的第二大招，通常也是最好用的。

很多网站会检测某一段时间某个IP的访问次数(通过流量统计，系统日志等)，如果访问次数多的不像正常人，它会禁止这个IP的访问。

所以我们可以设置一些代理服务器，每隔一段时间换一个代理，就算IP被禁止，依然可以换个IP继续爬取。

免费的开放代理获取基本没有成本，我们可以在一些代理网站上收集这些免费代理，测试后如果可以用，就把它收集起来用在爬虫上面。

免费短期代理网站举例：
    西刺免费代理IP
    快代理免费代理
    Proxy360代理
    全网代理IP

代理池： 
	如果代理IP足够多，形成代理池，就可以像随机获取User-Agent一样，随机选择一个代理去访问网站。
	
import urllib.request
import random

# 假设此时有一已经格式化好的ip代理地址proxies
# 可访问西刺代理获取代理ip：http://www.xicidaili.com/

# ip代理池
iplist = [
    "http://183.159.84.198:18118",
    "http://183.159.92.206:18118",
    "http://119.179.209.43:61234",
    "http://183.159.82.181:18118"
]

# ua池（user-agent池 ）
UserAngentList=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36"
]

url = 'https://blog.csdn.net/linangfs/article/details/78331419?locationNum=9&fps=1'

for i in range(3):
    headers = { "User-Agent": random.choice(UserAngentList)}
    proxy = {"http": random.choice(iplist)}
    
    try:
    	proxy_handler = urllib.request.ProxyHandler(proxy)
		opener = urllib.request.build_opener(proxy_handler)
		req = urllib.request.Request(url, headers=headers)
		response = opener.open(req)  # 使用代理
		print(response.code)

    except:
        print('失败')
    else:
        print('成功')

```


