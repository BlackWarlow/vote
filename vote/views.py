import datetime
from vote.models import *
from vote.forms import *

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from django.db import IntegrityError

from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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

def contacts_page(request):
    context= get_base_context(request)
    context['title']= 'Контакты - SV'
    context['main_header'] = 'Simple votings - Контакты'
    return render(request, 'contacts.html',context)

def polls_page(request):
    context = get_base_context(request)
    context['title'] = 'Список опросов - SV'
    context['main_header'] = 'Список опросов на сайте'
    all_polls = Poll.objects.all()
    lst = []
    max_polls = min(30, len(all_polls))
    for i in range(0, max_polls):
        lst.append(
            [Poll_variant.objects.filter(
                belongs_to=all_polls[i]),
             all_polls[i]]
        )
    context['polls'] = lst
    return render(request, 'polls/polls.html', context)


@login_required(login_url='/accounts/login/')
def my_polls(request):
    context = get_base_context(request)
    context['title'] = 'Мои опросы - SV'
    context['main_header'] = 'Список моих опросов'

    lst = []
    all_polls = Poll.objects.filter(author=request.user)
    for i in range(0, len(all_polls)):
        lst.append(
            [Poll_variant.objects.filter(
                belongs_to=all_polls[i]),
             all_polls[i]]
        )
    context['polls'] = lst
    return render(request, 'polls/polls.html', context)


def view_poll(request, id):
    context = get_base_context(request)
    try:
        poll = Poll.objects.filter(id=id)[0]
    except IndexError:
        raise Http404
    context['title'] = poll.name
    context['main_header'] = 'Просмотр опроса'

    all_variants = Poll_variant.objects.filter(belongs_to=poll)

    lst = []
    lst.append(all_variants)
    lst.append(poll)
    lst.append([i for i in range(0, len(all_variants))])
    context['polls'] = lst

    if request.method == 'POST':
        for i in range(0, len(all_variants)):
            st = 'variant_' + str(i)
            if request.POST[st]:
                print('qiw')
    return render(request, 'polls/poll.html', context)


@login_required(login_url='/accounts/login/')
def poll_create_page(request):
    context = get_base_context(request)
    context['title'] = 'Создать опрос - SV'
    context['main_header'] = 'Создание опроса'

    if request.method == 'POST':
        # create form
        form = Create_Poll(request.POST)

        if form.is_valid():
            # Poll name
            p_name = form.cleaned_data['name']

            # Poll object
            pollobj = Poll(date=context['current_date'],
                           name=p_name, author=request.user)
            pollobj.save()
            poll_id = pollobj.id

            # Writing poll objects
            for i in range(1, 11):
                st = 'variant_' + str(i)
                cur_name = form.cleaned_data[st]
                if cur_name == '':
                    done = True
                else:
                    Poll_variant(variant_name=cur_name,
                                 belongs_to=pollobj).save()
            context['form'] = form
            messages.add_message(
                request, messages.INFO, 'Опрос добавлен.')
            return redirect('/poll/' + str(poll_id) + '/')
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
            formm = User_Auth(request.POST)
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
            context["form"] = User_Auth()
    return render(request, "accounts/login.html", context)


@login_required(login_url='/accounts/login/')
def user(request):
    context = get_base_context(request)
    context['title'] = 'Аккуант - SV'
    context['main_header'] = 'Информация об аккаунте:'
    return render(request, 'accounts/user.html', context)


@login_required(login_url='/accounts/login/')
def user_edit(request):
    context = get_base_context(request)
    context['title'] = 'Редактирование аккаунта - SV'
    context['main_header'] = 'Редактировать аккаунт'

    if request.method == 'POST':
        form = User_Edit_Form(request.POST)
        user = request.user
        if form.is_valid():

            new_passwd = form.cleaned_data['new_password']
            new_username = form.cleaned_data['username']
            new_email = form.cleaned_data['email']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']

            if new_passwd:
                if user.check_password(form.cleaned_data['password']):
                    user.set_password(new_passwd)

            if new_username:
                user.username = new_username

            if new_email:
                user.email = new_email

            if new_first_name:
                user.first_name = new_first_name

            if new_last_name:
                user.last_name = new_last_name

            try:
                user.save()
            except IntegrityError:
                context['errors'] = 'Пользователь с таким именем уже существует!'
            else:
                messages.add_message(
                    request, messages.INFO, 'Изменения сохранены')
                return redirect('/accounts/user/')
        else:
            context['errors'] = 'Проверьте правильность заполнения полей!'
        context['form'] = form
    else:
        context['form'] = User_Edit_Form()

    return render(request, 'accounts/edit.html', context)

def user_register(request):
    context = get_base_context(request)
    context['title'] = 'Регистрация - SV'
    context['main_header'] = 'Регистрация на сайте'

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            email_form = User_Email_Form(request.POST)
            if form.is_valid() and email_form.is_valid():
                new_user = form.save()
                new_user.email = email_form.cleaned_data['email']
                new_user.save()
                messages.add_message(
                    request, messages.INFO, 'Вы зарегестрированы на сайте, войдите, чтобы продолжить')
                return redirect("/accounts/login/")
            else:
                errs = form.errors
                lst = []
                if 'username' in errs:
                    lst.append(
                       'Пользователь с таким ником уже существует')
                if 'password2' in errs:
                    lst.append(
                       'Пароли не удовлетворяют критериям безопасности или не совпадают')
                context['errors'] = lst
            context['form'] = form
            context['email_form'] = email_form
        else:
            context['form'] = UserCreationForm()
            context['email_form'] = User_Email_Form()
    return render(request, 'accounts/register.html', context)


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Вы вышли из аккаунта.')
    return redirect("main-page")


@login_required(login_url='/accounts/login/')
def add_report(request, id=1):
    context = get_base_context(request)
    context['title'] = 'Оставить жалобу - SV'

    if request.method == 'POST':
        form = Report_Form(request.POST)
        if form.is_valid():
            poll = Poll.objects.filter(id=form.cleaned_data['poll_id'])
            record = Report_Model(
                theme=form.cleaned_data['theme'],
                text=form.cleaned_data['text'],
                user=request.user,
                poll_id=poll,
            )
            record.save()
            messages.add_message(
                request, messages.INFO, 'Ваша жалоба отправлена администраторам')
    else:
        context['form'] = Report_Form()
        context['form'].poll_id = id
    return render(request, 'polls/add_report.html', context)

