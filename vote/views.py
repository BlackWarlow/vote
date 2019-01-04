import datetime
from vote.models import *
from vote.forms import *

from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def get_base_context(request):
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/pools/create/', 'text': 'Создать опрос'},
            {'link': '/pools/', 'text': 'Опросы'},
            {'link': '/pools/edit/', 'text': 'Редактировать опрос'},
            {'link': '/accounts/user/', 'text': 'Аккаунт'},
            {'link': '/accounts/logout/', 'text': 'Выйти'} if request.user.is_authenticated else
            {'link': '/accounts/login/', 'text': 'Войти'},
            {'link': '/creators/', 'text': 'Создатели'},
        ],

        'current_date': datetime.datetime.now().date(),
        'current_time': datetime.datetime.now().time(),
    }
    return context

def index_page(request):
    context = get_base_context(request)
    context['title'] = 'Главная страница - Simple Votings'
    context['main_header'] = 'Simple votings'
    return render(request, 'index.html', context)

def creators_page(request):
    context = get_base_context(request)
    context['title'] = 'SV - Создатели'
    context['main_header'] = 'Simple votings - The Django project by "The Blade Of Knowledge"'
    context['authors'] = Author.objects.all()
    return render(request, 'creators.html', context)


def pools_page(request):
    context = get_base_context(request)
    context['title'] = 'SV - Список опросов'
    context['main_header'] = 'Список опросов на сайте'
    all_pools = Pool.objects.all()
    lst = []
    for i in range(0, len(all_pools)):
        lst.append([Pool_variant.objects.filter(belongs_to=all_pools[i]), all_pools[i]])
    context['pools'] = lst
    return render(request, 'pools.html', context)

@login_required(login_url='/accounts/login/')
def pool_create_page(request):
    context = get_base_context(request)
    context['title'] = 'SV - Создать опрос'
    context['main_header'] = 'Создание опроса'
    if request.method == 'POST':
        # create form
        form = Create_Pool(request.POST)
        if form.is_valid():
            # if everything is valid get the data
            p_name = form.data['name']
            first_variant = form.data['first_variant']
            second_variant = form.data['second_variant']
            usr = User.objects.filter(id=request.user.id)[0]
            item = Pool(time=context['current_time'], date=context['current_date'],
                        name=p_name, author=usr)
            item.save()
            item1 = Pool_variant(variant_name=first_variant,
                                 votes=0, belongs_to=item)
            item1.save()
            item2 = Pool_variant(variant_name=second_variant,
                                 votes=0, belongs_to=item)
            item2.save()
        context['form'] = form
    else:
        context['form'] = Create_Pool()
    return render(request, 'create.html', context)


def login(request):
    context = get_base_context(request)
    if request.user.is_authenticated:
        # if user is logged in
        context["logged_in"] = True
    else:
        if request.method == "POST":
            # if user is entered something in the form
            formm = User_auth(request.POST)
            if formm.is_valid():
                # if everything is entered as it should be
                user = authenticate(request, username=request.POST["username"],
                                   password=request.POST["password"])
                if user is not None:
                    # if user exists login
                    login(request, usr)
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
    return render(request, "login.html", context)


@login_required(login_url='/accounts/login/')
def user(request):
    context = get_base_context(request)
    context['main_header'] = 'Информация об аккаунте:'
    context['username'] = request.user.username
    context['user_mail'] = request.user.email
    context['user_status'] = 'Бог'
    return render(request, 'user.html', context)

@login_required(login_url='/accounts/login/')
def logout(request):
    context = get_base_context(request)
    logout(request)
    return render(request, "logout.html", context)