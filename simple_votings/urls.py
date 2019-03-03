"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth

from vote import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index_page, name='main-page'),
    path('creators/', views.creators_page),

    path('polls/', views.polls_page),
    path('polls/my_polls/', views.my_polls),
    path('polls/create/', views.poll_create_page),
    path('poll/<str:hash_id>/', views.view_poll),
    # TODO path('poll/edit/<str:hash_id>/', views.edit_poll),

    path('polls/add_report/', views.add_report),
    path('polls/add_report/<str:hash_id>/', views.add_report),
    path('polls/my_reports/', views.my_reports),

    path('accounts/login/', views.login_page),
    path('accounts/logout/', views.logout_page),
    path('accounts/user/', views.user),
    path('accounts/user/<int:user_id>/', views.user),
    path('accounts/edit/', views.user_edit),
    path('accounts/register/', views.user_register),
    path('contacts/', views.contacts_page),
    path('donate/', views.donate_page),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
