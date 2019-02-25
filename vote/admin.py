from django.contrib import admin

# Register your models here.
from vote.models import Poll, Poll_variant, Blog_Model


class PollVariantsInline(admin.TabularInline):
    model = Poll_variant
    extra = 0

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'hash_id', 'date', 'open_date', 'time',
                    'name', 'one_answer', 'author', 'open_for_vote')
    list_filter = ('id', 'hash_id', 'date', 'open_date', 'time',
                   'name', 'one_answer', 'author', 'open_for_vote')
    fields = [('name', 'date', 'open_date', 'time'),
               ('hash_id', 'one_answer'), 'author', 'open_for_vote']
    inlines = [PollVariantsInline]

@admin.register(Blog_Model)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'date', 'author', 'content')
    list_filter = ('id', 'theme', 'date', 'author')
    fields = [('author', 'date'), ('theme', 'content')]
