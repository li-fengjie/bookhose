# 上下文 处理器  

> 返回一些数据 在全局模板中都可以使用 比如登录以后的用户信息  在很多页面上都可以使用  这时候不需要
>
> 在每个视图函数中返回  

```python
django.template.context_processors.debug

这个上下文做的是 查看 本视图函数执行了哪些sql 操作   

需要在settings.py 中设置  debug = True  
INTERNAL_IPS = ['127.0.0.1']

然后直接在页面上 使用    {{debug}} {{sql_queries}} {{是否开启了debug}}/{{该页面执行的sql语句}}


'django.template.context_processors.request',  直接在模板中  {{request.path}} 可以查看本视图函数的 路由  

'django.template.context_processors.media',
<img src="{{ MEDIA_URL }}mtv.png" alt="">  直接在页面上 这么使用即可 前提是  settings中设置了  MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
而且 

urls.py中: 
    from django.conf.urls.static import static
    from django.conf import settings
    urlpatterns = [
    path('', views.index,name='index'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



'django.template.context_processors.csrf', 
    <meta name="csrf_token" content="{{ csrf_token }}"> 直接在页面上使用 即可  
```





## 中间件   

request 到 response 处理过程中的一个插件  比如 请求到达视图函数之前  我先判断用户是否登录   

登录了将 user对象绑定到了 request上   

