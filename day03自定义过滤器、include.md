### 自定义过滤器  

1.在指定的应用下面  （先要注册到 INSTALLED_APPS） 创建一个 python包  templatetags  然后再包中再创建一个python文件用来存放我们的过滤器  

2.在文件中写过滤器 写完了要记得注册  

```
from django import template
from datetime import datetime
register = template.Library()


@register.filter #将过滤器注册到系统中
def time_since(value):
    # 小于1分钟显示刚刚
    #小于一个小时  X分钟以前
    #小于24 小时  X小时以前
    #小于30天  X天前
    #其它时间显示 年月日
    if not isinstance(value,datetime):
        return value
    now = datetime.now()
    timestamp = (now-value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp > 60 and timestamp < 60*60:
        minutes = int(timestamp/60)
        return "%s 分钟以前" % minutes
    elif timestamp > 60*60 and timestamp < 60*60*24:
        hours = int(timestamp/60/60)
        return "%s 小时以前" % hours
    elif timestamp > 60*60*24 and timestamp < 60*60*24*30:
        day = int(timestamp/60/60/24)
        return "%s 天以前" % day
    else:
        return value.strftime("%Y/%m/%d %H:%M")

```

3.页面上   

```
{% load my_filter %} #加载 存放过滤器的文件
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>index</title>
</head>
<body>
    {{ mytime | time_since }}
</body>
</html>
```



### 模板  include  

```
index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
    {% include 'header.html' %}
    <div class="content">
        这是中间的内容 {{ username }}
    </div>
    {% include 'footer.html' %}
</body>
</html>

header.html

<header>
    <ul>
        <li><a href="/">首页</a></li>
        <li><a href="{% url 'company' %}">公司</a></li>
        <li><a href="{% url 'school' %}">校园</a></li>
        <li>{{ username }}</li>
    </ul>
</header>



company.html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>company</title>
</head>
<body>
    {% include 'header.html' with username="kangbazi" %}
    公司
    {% include 'footer.html' %}

</body>
</html>

```



## 模板继承 

```
# 模版继承笔记：

在前端页面开发中。有些代码是需要重复使用的。这种情况可以使用`include`标签来实现。也可以使用另外一个比较强大的方式来实现，那就是模版继承。模版继承类似于`Python`中的类，在父类中可以先定义好一些变量和方法，然后在子类中实现。模版继承也可以在父模版中先定义好一些子模版需要用到的代码，然后子模版直接继承就可以了。并且因为子模版肯定有自己的不同代码，因此可以在父模版中定义一个block接口，然后子模版再去实现。以下是父模版的代码：

​```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
<link rel="stylesheet" href="{% static 'style.css' %}" />
<title>{% block title %}我的站点{% endblock %}</title>
</head>

<body>
<div id="sidebar">
{% block sidebar %}
<ul>
<li><a href="/">首页</a></li>
<li><a href="/blog/">博客</a></li>
</ul>
{% endblock %}
</div>
<div id="content">
{% block content %}{% endblock %}
</div>
</body>
</html>
​```

这个模版，我们取名叫做`base.html`，定义好一个简单的`html`骨架，然后定义好两个`block`接口，让子模版来根据具体需求来实现。子模板然后通过`extends`标签来实现，示例代码如下：

​```html
{% extends "base.html" %}

{% block title %}博客列表{% endblock %}

{% block content %}
{% for entry in blog_entries %}
<h2>{{ entry.title }}</h2>
<p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
​```

**需要注意的是：extends标签必须放在模版的第开始的位置**
**子模板中的代码必须放在block中，否则将不会被渲染。**
如果在某个`block`中需要使用父模版的内容，那么可以使用`{{block.super}}`来继承。比如上例，`{%block title%}`，如果想要使用父模版的`title`，那么可以在子模版的`title block`中使用`{{ block.super }}`来实现。

在定义`block`的时候，除了在`block`开始的地方定义这个`block`的名字，还可以在`block`结束的时候定义名字。比如`{% block title %}{% endblock title %}`。这在大型模版中显得尤其有用，能让你快速的看到`block`包含在哪里。
```

