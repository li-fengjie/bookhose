from django.contrib.auth import authenticate, login
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.hashers import check_password

from apps.cms.models import User, Book, Author, Catalog, Content
from apps.front.forms import RegisterForm, MyLoginForm
from utils import restful
from django.http import HttpResponse


def send(mobile, captcha):
    url = 'http://v.juhe.cn/sms/send'
    params = {
        "mobile": mobile,
        "tpl_id": 135629,
        "tpl_value": "#code#=" + captcha,
        "key": "",
    }

    response = requests.get(url=url, params=params)
    result = response.json()
    print(result)
    if result['error_code'] == 0:
        return True
    else:
        return False


class RegisterView(View):
    def get(self, request):
        messages = {"messages": ""}
        return render(request, 'register.html', messages)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password1')
            user = User.objects.create(username=username, telephone=telephone)
            user.set_password(password)
            user.save()
            # form.save()
            return redirect(reverse('index'))
        else:
            print(form.errors.get_json_data())
            messages = {"messages": form.errors.get_json_data()}
            # return redirect(reverse('register'))
            return render(request, 'register.html', messages)


class LoginView(View):
    def get(self, request, **kwargs):
        messages = {'messages': ''}
        return render(request, 'login.html', messages)

    # require_POST
    def post(self, request, **kwargs):
        form = MyLoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            print(telephone + " " + password)
            user = authenticate(request, telephone=telephone, password=password)
            print(user)
            if user:
                if user.is_active:
                    request.session['telephone'] = user.telephone;
                    request.session['id'] = user.id;
                    login(request, user)
                    # return restful.ok()
                    return redirect(reverse('index'))
                else:
                    messages = {'messages': '您的账户已经被冻结啦'}
                    # return restful.unauth_error(message="您的账户已经被冻结啦")
                    return render(request, 'login.html', messages)
            else:
                # return restful.params_error(message="手机号或者密码错误")
                messages = {'messages': '手机号或者密码错误'}
                return render(request, 'login.html', messages)

        else:
            errors = form.get_errors()
            # return restful.params_error(message=errors)
            messages = {"messages": form.get_errors()}
            return render(request, 'login.html', messages)


def logout(request):
    request.session.flush()
    return redirect(reverse('index'))


def index(request):
    return render(request, 'index.html')


def free(request):
    books = Book.objects.all()
    return render(request, 'free.html', context={"books": books})


def fileend(request):
    return render(request, 'fileend.html')


def serial(request):
    return render(request, 'fileend.html')

def mybooks(request,id):
    print(id)
    user = User.objects.get(id__exact=id)
    # print(user.collection)
    books = user.collection.all()

    # TODO
    return render(request,'mybooks.html',context={"books":books})

import requests

def collection(request,id):
    user = User.objects.get(id__exact=request.session.get('id'))
    book = Book.objects.get(id__exact=id)
    user.collection.add(book)
    # book.tag.add(*tags)
    print(book)
    return HttpResponse("<a class=\"border-btn add-book\" style=\"border-color: palegreen;color: #000000\">我的阅读</a>")

def send():
    clean_data = super(RegisterForm).clean()
    telephone = clean_data.get('telephone')
    url = 'http://v.juhe.cn/sms/send'
    params = {
        "mobile": telephone,
        "tpl_id": 167978,
        "tpl_value": "#code#=" + 5586,
        "key": "e263766ba0d791c3abd97070bd969a05",
    }

    response = requests.get(url=url, params=params)
    result = response.json()
    print(result)
    if result['error_code'] == 0:
        return True
    else:
        return False


from django.db import connection


# Create your views here.
def get_cursor():
    return connection.cursor()


def book_catalog(request, book_id):
    print(book_id)
    # catalogs
    # book
    book = Book.objects.get(id__exact=book_id)
    catalogs = Catalog.objects.filter(book=book).order_by('index')
    print(catalogs)
    return render(request, 'catalog.html', context={"book": book, "catalogs": catalogs})


def book_detail(request, content_id):
    print(content_id)
    content = Content.objects.get(id__exact=content_id)
    print(content)
    return render(request, 'detail.html', context={"content": content})
