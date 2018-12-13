import datetime
from vote.models import Author

from django.shortcuts import render

def get_base_context():
    context = {
        'menu': [
            {'link': '/', 'text': 'Главная'},
            {'link': '/creators', 'text': 'Создатели'},
            {'link': '/pools/', 'text': 'Опросы'}
        ],
        'current_time': datetime.datetime.now(),
    }
    return context

def index_page(request):
    context = get_base_context()
    context['title'] = 'Главная страница - Simple Votings'
    context['main_header'] = 'Simple votings'
    return render(request, 'index.html', context)

def creators_page(request):
    context = get_base_context()
    context['title'] = 'SV - Создатели'
    context['main_header'] = 'Simple votings - The Django project by "The Blade Of Knowledge"'
    context['authors'] = Author.objects.all()
    return render(request, 'creators.html', context)

def pools_page(request):
    context = get_base_context()
    context['title'] = 'SV - Список опросов'
    context['main_header'] = 'Список опросов на сайте'
    return render(request, 'pools.html', context)
