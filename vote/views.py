import datetime
from vote.models import *
from vote.forms import *

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse

def get_base_context(request):
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/pools/create/', 'text': 'Создать опрос'},
            {'link': '/pools/', 'text': 'Опросы сайта'},
            {'link': '/accounts/user/', 'text': 'Аккаунт'},
            {'link': '/my_pools/', 'text': 'Мои опросы'},
            {'link': '/accounts/logout/', 'text': 'Выйти'},
            {'link': '/accounts/login/', 'text': 'Войти'},
            {'link': '/accounts/edit/', 'text': 'Редактировать'},
            {'link': '/creators/', 'text': 'О нас'},
            {'link': '/contacts/', 'text': 'Контакты'},
            {'link': '/donate/', 'text': 'Помощь'},
        ],
        'user': request.user,
        'current_date': datetime.datetime.now().date().__str__(),
        'current_time': datetime.datetime.now().time().__str__()[:8],
    }
    return context

def index_page(request):
    context = get_base_context(request)
    context['title'] = 'Главная страница - SV'
    context['main_header'] = 'Simple votings'
    return render(request, 'index.html', context)

def creators_page(request):
    context = get_base_context(request)
    context['title'] = 'Создатели - SV'
    context['main_header'] = 'Simple votings - Django Python проект группы "Лезвие знаний"'
    context['authors'] = Author.objects.all()
    return render(request, 'creators.html', context)


def pools_page(request):
    context = get_base_context(request)
    context['title'] = 'Список опросов - SV'
    context['main_header'] = 'Список опросов на сайте'
    all_pools = Pool.objects.all()
    lst = []
    for i in range(0, len(all_pools)):
        lst.append([Pool_variant.objects.filter(belongs_to=all_pools[i]), all_pools[i]])
    context['pools'] = lst
    return render(request, 'pools/pools.html', context)


@login_required(login_url='/accounts/login/')
def pool_create_page(request):
    context = get_base_context(request)
    context['title'] = 'Создать опрос - SV'
    context['main_header'] = 'Создание опроса'

    if request.method == 'POST':
        # create form
        form = Create_Pool(request.POST)

        if form.is_valid():
            # Pool name
            p_name = form.data['name']

            # Pool object
            poolobj = Pool(date=context['current_date'], name=p_name, author=request.user)
            poolobj.save()

            # Writing pool objects
            for i in range(1, 11):
                st = 'variant_' + str(i)
                cur_name = form.data[st]
                if cur_name == '':
                    done = True
                else:
                    Pool_variant(variant_name=cur_name, votes=0,
                                 belongs_to=poolobj).save()
            context['form'] = form
        else:
            context['form'] = form
    else:
        # If we didn't had any data
        context['form'] = Create_Pool()
    return render(request, 'pools/create.html', context)


def login_page(request):
    context = get_base_context(request)
    context['title'] = 'Войти - SV'
    context['main_header'] = 'Вход на сайт'

    if not request.user.is_authenticated:
        if request.method == "POST":
            # if user is entered something in the form
            formm = User_auth(request.POST)
            if formm.is_valid():
                # if everything is entered as it should be
                user = authenticate(request, username=request.POST["username"],
                                   password=request.POST["password"])
                if user is not None:
                    # if user exists login
                    login(request, user)
                    messages.add_message(
                        request, messages.INFO, 'Вы успешно авторизовались.')
                    return redirect(reverse('main-page'))
                else:
                    # if password or username is not valid
                    context["error"] = True
            else:
                # if entered data is not valid
                context["error"] = True
            # setting displayed form
            context["form"] = formm
        else:
            # setting new form
            context["form"] = User_auth()
    return render(request, "accounts/login.html", context)


@login_required(login_url='/accounts/login/')
def user(request):
    context = get_base_context(request)
    context['main_header'] = 'Информация об аккаунте:'
    context['username'] = request.user.username
    context['user_mail'] = request.user.email
    context['user_status'] = ''
    return render(request, 'accounts/user.html', context)


def logout_page(request):
    logout(request)
    return redirect("main-page")
    # return render(request, "logout.html", context)


@login_required(login_url='/accounts/login/')
def add_report(request):
    context = {
        'pagename': "Оставить жалобу"
    }
    user = User.objects.get()

    if request.method == 'POST':
        form = ReForm(request.POST)
        if form.is_valid():
            record = ReModel(
                type=form.data['type'],
                text=form.data['text'],
                user=user
            )
            record.save()
            context['addform'] = ReForm()
    else:
        context['addform'] = ReForm()
    return render(request, 'pages/add_report.html', context)

