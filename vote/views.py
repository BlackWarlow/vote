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
            {'link': '/polls/create/', 'text': 'Создать опрос'},
            {'link': '/polls/', 'text': 'Опросы сайта'},
            {'link': '/accounts/user/', 'text': 'Аккаунт'},
            {'link': '/my_polls/', 'text': 'Мои опросы'},
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
    all_polls = Poll.objects.all()
    lst = []
    for i in range(0, len(all_pools)):
        lst.append(
            [Poll_variant.objects.filter(
                belongs_to=all_polls[i]),
             all_polls[i]]
        )
    context['polls'] = lst
    return render(request, 'polls/polls.html', context)


@login_required(login_url='/accounts/login/')
def pool_create_page(request):
    context = get_base_context(request)
    context['title'] = 'Создать опрос - SV'
    context['main_header'] = 'Создание опроса'

    if request.method == 'POST':
        # create form
        form = Create_Poll(request.POST)

        if form.is_valid():
            # Poll name
            p_name = form.data['name']

            # Poll object
            pollobj = Poll(date=context['current_date'],
                           name=p_name, author=request.user)
            pollobj.save()

            # Writing poll objects
            for i in range(1, 11):
                st = 'variant_' + str(i)
                cur_name = form.data[st]
                if cur_name == '':
                    done = True
                else:
                    Poll_variant(variant_name=cur_name, votes=0,
                                 belongs_to=pollobj).save()
            context['form'] = form
        else:
            context['form'] = form
    else:
        # If we didn't have any data
        context['form'] = Create_Poll()
    return render(request, 'polls/create.html', context)


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

@login_required(login_url='/accounts/login/')
def user_edit(request):
    context = get_base_context(request)
    return render(request, '', context)


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Вы вышли из аккаунта.')
    return redirect("main-page")
    # return render(request, "logout.html", context)


@login_required(login_url='/accounts/login/')
def add_report(request):
    context = {
        'title': "Оставить жалобу - SV"
    }
    user = User.objects.get()

    if request.method == 'POST':
        form = ReporrtForm(request.POST)
        if form.is_valid():
            record = ReModel(
                type=form.data['type'],
                text=form.data['text'],
                user=user
            )
            record.save()
            context['addform'] = ReportForm()
    else:
        context['addform'] = ReportForm()
    return render(request, 'polls/add_report.html', context)

