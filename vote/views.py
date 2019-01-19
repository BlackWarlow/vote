import datetime
from vote.models import *
from vote.forms import *

from django.shortcuts import render

def get_base_context(request):
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/creators', 'text': 'Создатели'},
            {'link': '/pools', 'text': 'Опросы'},
            {'link': '/create', 'text': 'Создать опрос'}
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
    all_pools = Pool.objects.all()
    lst = []
    for i in range(0, len(all_pools)):
        lst.append([Pool_variant.objects.filter(belongs_to=all_pools[i]), all_pools[i]])
    context['pools'] = lst
    return render(request, 'pools.html', context)

def pool_create_page(request):
    context = get_base_context(request)
    context['title'] = 'SV - Создать опрос'
    context['main_header'] = 'Создание опроса'

    if request.method == 'POST':
        # If we have some data back
        form = Create_Pool(request.POST)

        if form.is_valid():
            # Pool name
            p_name = form.data['name']

            # User object
            usr = User.objects.filter(username='usr')[0]

            # Pool object
            poolobj = Pool(date=context['current_time'], name=p_name, author=usr)
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
    return render(request, 'create.html', context)

def pool(request):
    context = get_base_context()
    return render(request, 'pool.html', context)
