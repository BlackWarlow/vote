import datetime
import hashlib

from vote.models import *
from vote.forms import *

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

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
            {'link': '/polls/my_polls/', 'text': 'Мои опросы'},
            {'link': '/accounts/logout/', 'text': 'Выйти'},
            {'link': '/accounts/login/', 'text': 'Войти'},
            {'link': '/accounts/edit/', 'text': 'Редактировать'},
            {'link': '/creators/', 'text': 'О нас'},
            {'link': '/contacts/', 'text': 'Контакты'},
            {'link': '/donate/', 'text': 'Помощь'},
            {'link': '/admin/', 'text': 'Модерация'},
            {'link': '/polls/my_reports', 'text': 'Мои жалобы'}
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
    context['blogs'] = list(reversed(Blog_Model.objects.all()))
    return render(request, 'index.html', context)

def creators_page(request):
    context = get_base_context(request)
    context['title'] = 'Создатели - SV'
    context['main_header'] = 'Simple votings - Django Python проект группы "Лезвие знаний"'
    context['authors'] = list(reversed(Author.objects.all()))
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
    max_polls = min(20, len(all_polls))

    lst = []
    for i in range(0, max_polls):
        lst.append(
            [
                Poll_variant.objects.filter(belongs_to=all_polls[i]),
                all_polls[i]
            ]
        )
    context['polls'] = list(reversed(lst))
    return render(request, 'polls/polls.html', context)


@login_required(login_url='/accounts/login/')
def my_polls(request):
    context = get_base_context(request)
    context['title'] = 'Мои опросы - SV'
    context['main_header'] = 'Список моих опросов'
    all_polls = Poll.objects.filter(author=request.user)

    lst = []
    for i in range(0, len(all_polls)):
        lst.append(
            [
                Poll_variant.objects.filter(belongs_to=all_polls[i]),
                all_polls[i]
            ]
        )
    context['polls'] = list(reversed(lst))
    return render(request, 'polls/polls.html', context)


def view_poll(request, hash_id):
    context = get_base_context(request)
    poll = get_object_or_404(Poll, hash_id=hash_id)

    if poll.open_for_vote:
        if datetime.datetime.now().date() > poll.open_date:
            if datetime.datetime.now().time() > poll.time:
                poll.open_for_vote = False
                poll.save()

    context['title'] = poll.name
    context['main_header'] = 'Просмотр опроса'
    context['poll_hash'] = hash_id

    all_variants = Poll_variant.objects.filter(belongs_to=poll)
    voted = False

    # Checking if already voted and getting all votes
    for i in range(len(all_variants)):
        if len(Vote.objects.filter(author=request.user, belongs_to=all_variants[i])):
            voted = True

    # Voting for variants
    if request.method == 'POST' and not voted and poll.open_for_vote:
        if poll.one_answer:
            variant = request.POST.get('poll')[-1:]
            vote = Vote(
                belongs_to=all_variants[int(variant)],
                author=request.user
            )
            vote.save()
        else:
            lst = []
            for i in range(0, 10):
                variant = request.POST.get('variant_' + str(i))
                if variant == 'on':
                    vote = Vote(
                        belongs_to=all_variants[i],
                        author=request.user
                    )
                    vote.save()
        voted = True

    # Renewing votes
    all_votes = 0
    for i in range(len(all_variants)):
        all_votes += len(Vote.objects.filter(belongs_to=all_variants[i]))

    # Getting and reworking data
    lst = []
    for i in range(len(all_variants)):
        votes = len(Vote.objects.filter(belongs_to=all_variants[i]))

        if all_votes == 0:
            all_votes = 1

        vote = votes / all_votes * 100
        tmp_lst = [all_variants[i], str(round(vote, 1)) + '%', i, round(vote, 0)]
        lst.append(tmp_lst)


    context['poll_variants'] = lst
    context['poll'] = poll
    context['voted'] = voted
    context['closed'] = not poll.open_for_vote
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
            one_var = form.cleaned_data['one_variant']
            open_date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            # Poll object
            pollobj = Poll(
                one_answer=one_var,
                date=context['current_date'],
                name=p_name,
                author=request.user,
                open_date=open_date,
                time=time,
            )
            pollobj.save()
            id_str = str(pollobj.id)
            pollobj.hash_id = hashlib.shake_128(
                bytes(id_str, 'utf-8')).hexdigest(5)
            pollobj.save()

            # Writing poll variant objects
            for i in range(1, 11):
                st='variant_' + str(i)
                cur_name=form.cleaned_data[st]
                if cur_name == '':
                    done=True
                else:
                    Poll_variant(
                        variant_name=cur_name,
                        belongs_to=pollobj
                    ).save()
            context['form']=form
            messages.add_message(
                request,
                messages.INFO,
                'Опрос добавлен.'
            )
            return redirect('/poll/' + str(pollobj.hash_id) + '/')
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
def user(request, user_id=None):
    context = get_base_context(request)
    context['title'] = 'Аккаунт - SV'
    context['main_header'] = 'Информация об аккаунте:'
    context['guest'] = False
    if user_id is not None:
        context['guest'] = True
        context['user'] = get_object_or_404(User, id=user_id)
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
def add_report(request, hash_id):
    context = get_base_context(request)
    context['title'] = 'Оставить жалобу - SV'
    context['main_header'] = 'Создание жалобы'

    if request.method == 'POST':
        form = Report_Form(request.POST)
        if form.is_valid():
            try:
                poll = Poll.objects.filter(
                    hash_id=form.cleaned_data['poll_hash_id'])[0]
            except IndexError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Извините, такого опроса не существует.'
                )
                context['form'] = Report_Form()
                render(request, 'reports/add_report.html', context)
            else:
                record = Report_Model(
                    theme=form.cleaned_data['theme'],
                    text=form.cleaned_data['text'],
                    user=request.user,
                    poll=poll,
                )
                record.save()
                messages.add_message(
                    request, messages.INFO, 'Ваша жалоба отправлена администраторам')
                return redirect('/poll/' + hash_id + '/')
    else:
        context['form'] = Report_Form(initial={'poll_hash_id': hash_id})
        try:
            poll = Poll.objects.filter(
                hash_id=hash_id)[0]
            context['poll_name'] = poll.name
        except IndexError:
            pass
    return render(request, 'reports/add_report.html', context)

@login_required(login_url='/accounts/login/')
def my_reports(request):
    context = get_base_context(request)
    context['title'] = 'Мои жалобы - SV'
    context['main_header'] = 'Список моих жалоб'
    context['reports'] = list(
        reversed(Report_Model.objects.filter(user=request.user)))
    return render(request, 'reports/my_reports.html', context)

def donate_page(request):
    context = get_base_context(request)
    context['title'] = 'Поддержать - SV'
    context['main_header'] = 'Пожертвовать на благо проекта'
    return render(request, 'donate.html', context)
