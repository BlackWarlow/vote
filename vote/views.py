import datetime
from vote.models import *
from vote.forms import *

from django.shortcuts import render

def get_base_context(request):
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/creators', 'text': 'Создатели'},
            {'link': '/pools/', 'text': 'Опросы'},
            {'link': '/create/', 'text': 'Создать опрос'}
        ],
        'current_time': datetime.datetime.now(),
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
    context['pools'] = Pool_variant.objects.all()
    return render(request, 'pools.html', context)

def pool_create_page(request):
    context = get_base_context(request)
    context['title'] = 'SV - Создать опрос'
    context['main_header'] = 'Создание опроса'
    if request.method == 'POST':
        form = Create_Pool(request.POST)
        if form.is_valid():
            p_name = form.data['name']
            first_variant = form.data['first_variant']
            second_variant = form.data['second_variant']
            usr = User.objects.filter(username='usr')[0]
            item = Pool(date=context['current_time'],
                        name=p_name, author=usr)
            item.save()
            item1 = Pool_variant(variant_name=first_variant,
                                 votes=0, belongs_to=item)
            item1.save()
            item2 = Pool_variant(variant_name=second_variant,
                                 votes=0, belongs_to=item)
            item2.save()

            context['first_variant']=first_variant
            context['second_variant']=second_variant
            context['p_name'] = p_name
            context['form'] = form
        else:
            context['form'] = form
    else:
        context['form'] = Create_Pool()
    return render(request, 'create.html', context)
