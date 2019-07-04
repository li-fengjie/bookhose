from django.shortcuts import render, redirect
from django.urls import reverse
import uuid
# from apps.cms.form import MyForm
from django.views import View

from apps.cms.form import BookForm
from .models import State, Author, Tag, Catalog, Book, Content
from django.http import HttpResponse


# Create your views here.

# Create your tests here.
# -*- coding: utf-8 -*-
import urllib.request
import bs4
import re


# 模拟浏览器访问url并获取页面内容（即爬取源码）
# from apps.cms.models import State, Author, Tag, Content, Book, Catalog


def getHtml(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers = {"User-Agent": user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html


# 爬取整个网页（这里就细致一些，指定编码之类的）
def parse(url):
    html_doc = getHtml(url)
    sp = bs4.BeautifulSoup(html_doc, 'html.parser', from_encoding="utf-8")
    return sp


# 获取书籍目录（正式开始了）
def get_book_dir(url):
    books_dir = []
    name = parse(url).find('div', class_='listmain')
    cover = parse(url).find('img', class_='cover')
    intro = parse(url).find('div', class_='intro')

    if name:
        dd_items = name.find('dl')
        dt_num = 0
        for n in dd_items.children:
            ename = str(n.name).strip()
            if ename == 'dt':
                dt_num += 1
            if ename != 'dd':
                continue
            books_info = {}
            if dt_num == 2:
                durls = n.find_all('a')[0]
                books_info['name'] = (durls.get_text())
                books_info['url'] = 'http://www.biqukan.com' + durls.get('href')
                books_dir.append(books_info)
    return books_dir


# 获取章节内容
def get_charpter_text(curl):
    text = parse(curl).find('div', class_='showtxt')
    # if text:
    #     cont = text.get_text()
    #     cont = [str(cont).strip().replace('\r \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0', '').replace('\u3000\u3000', '')]
    #     c = " ".join(cont)
    #     ctext = re.findall(r'^.*?html', c)
    #     return ctext
    # else:
    #     return ''
    return text


# 获取书籍（目录和内容整合）
def get_book(burl):
    # 目录
    book = get_book_dir(burl)
    if not book:
        return book

    # 内容
    for d in book:
        curl = d['url']
        try:
            print('正在获取章节【{}】【内容】【{}】'.format(d['name'], d['url']))
            ctext = get_charpter_text(curl)
            d['text'] = ctext
            print(d['text'])
            # book1 = Book.objects.get(id__exact=1)
            # content = Content(content=d['text'])
            # content.save()
            # title = d['name']
            # catalog = Catalog(title=title, index=i, content=content,book=book1)
            # catalog.save()
            print()
        except Exception as err:
            d['text'] = 'get failed'
            print(err)

    return book

def add(request):
    book = get_book('http://www.biqukan.com/1_1094/')
    print(book)

    #
    # state = State(name="完结")
    # state.save()
    # author = Author(authorname="若雪飞扬")
    # author.save()
    # tag = Tag(name="浪漫青春")
    # tag1 = Tag(name="现代言情")
    # tag.save()
    # tag1.save()
    # tags = Tag.objects.filter(id__in=[1, 2])
    # print(tags)
    # content = Content(content="章节一内容")
    # content1 = Content(content="<p>　　“你从盛大华美的高潮里倒退，带我去听怦然心动的第一个音符。”</p><p>　　Chapter 1 </p><p>　　1</p><p>　　路边昏黄的路灯闪烁了一下，发出“兹拉”一声响，终于不再挣扎，彻底熄灭了。整条路都跟着暗下来，在夜色的衬托下，显得幽暗又清冷。一辆小车开过去，速度渐渐慢下来。</p><p>　　“张老板，上次我过来的时候也是这样，路灯都没有，一片漆黑的，”副驾驶座的小林说，“那天我越走越觉得不对劲……”</p><p>　　这个别墅区好像没什么人住，张老板也不是第一次来了，店里所有来送过外卖的人都说都没见到过这里有人进出，两个人渐渐有些发毛，小林突然注意到别墅区有一块异常明亮，他把车窗摇下来探出头说：“老板，你看那里是不是有人？”</p><p>　　张老板加快油门开近，发现正是他们送外卖的那栋别墅门口停了好几辆警车，还有几个民警在进进出出。</p><p>　　“干什么的？”他们的车很快被拦了下来，“办案呢，闲杂人等回避一下。”</p><p>　　“我们是来送餐的，”小林慌慌张张地问，“里面出什么事了？”</p><p>　　“死人了，”民警朝他们伸出手，“把单子拿出来我看看。”</p><p>　　小林赶紧把东西递过去，民警只扫了一眼，脸色就严肃起来：“这家人都死了一个礼拜了，两个小时前保洁才发现里面有恶臭报的警，怎么可能叫外卖？”</p><p>　　可怜张老板刚下车，听到这句直接腿一软就一屁股坐在了地上：“你、你说什么？都死了？”</p><p>　　“一家五口，死了有日子了，刚刚才被发现，”民警狐疑地看着他们，“真有人叫了你们家的吃的？跟我们回去做个笔录吧！”</p><p>　　正是盛夏时节，到了晚餐的点，谷记生意格外好，白琮百无聊赖地坐在一个靠窗的位置上，伸手拨弄了一下耳洞里藏着的接收器，听着里面传出来刺刺拉拉的电流声，对今晚这个任务实在提不起什么兴趣。</p><p>　　谷记是岳城有名的网红夜宵店，前两年上过几个综艺节目，知名度迅速打开了，成为许多游客必须打卡的一个地方，说是夜宵店，其实中午就开始营业了，这会儿小龙虾刚上市，再搭配他们店里特有的烧烤，虽然已经晚上十一点多了，还是非常热闹。可就是这么一家网红店，从上个月开始总是接到一个奇怪的外卖单，虽然现在各类外卖app都很方便，但谷记并没有搞这些活动，宵夜嘛，大多数时候吃的就是个气氛，尤其在露天的店外，大汗淋漓地喝着冰啤酒，要多爽有多爽，然而三月前的一个晚上开始，店里的座机总能接到一个奇怪的电话，要求送餐上门。</p><p>　　“我们谷记可是老字号了，平时要的就是店里这人多的热闹劲，哪家app平台都没合作，就留了一个绑定网线的座机，八百年没人打过了，也不知道他们上哪儿弄到的号码，本来我们是不肯的，之前从来没这规矩，”张老板报案的时候解释说，“可刚好那天我们生意不太好，他们叫的东西又多，这么大的单子……就破了一回例。”</p><p></p>")
    # content.save()
    # content1.save()
    # book = Book(title="Hi，我的草莓味少年", author=author, view_num=0,
    #             cover="cover/7-14041621494I41.png",
    #             instruction="青春高甜宠文，撩动你沉寂已久的少女心，那个曾经陪你上课的人，现在还在等你下班吗？ ◆高一那年，地铁站出口，她被一群不良少年围堵戏耍， 身为“不良少年头目”的他，从天而降，“英雄救美”。 临别时，她义正言辞地警告他：“以后别让你的",
    #             state=state)
    # book.save()
    # book.tag.add(*tags)
    #
    # catalog = Catalog(title="章节一", index=1, content=content,book=book)
    # catalog1 = Catalog(title="章节二", index=2, content=content1,book=book)
    # catalog1.save()
    # catalog.save()
    return HttpResponse("success")


def save_file(file):
    with open('somefile.txt', 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)


class AddbookView(View):
    def get(self, request):
        messages = {"messages": ""}
        return render(request, 'addbook.html', messages)

    def post(self, request):
        form=BookForm(request.POST,request.FILES)
        title = request.POST.get('title')
        instruction = request.POST.get('instruction')
        authorname = request.POST.get('author')
        author = Author(authorname=authorname)
        author.save()
        state = State.objects.first()
        cover = request.FILES.get('cover')
        print(cover)
        # cover.save()
        book = Book(title=title, author=author,
                    cover=cover,state=state,
                    instruction=instruction)
        book.save()
        messages = {"messages": "上传成功"}
        # form.save()
        return render(request, 'addbook.html',messages)
