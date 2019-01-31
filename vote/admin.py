from django.contrib import admin

# Register your models here.
from vote.models import Poll, Poll_variant


class PollVariantsInline(admin.TabularInline):
    model = Poll_variant
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'name', 'author')
    list_filter = ('id', 'date', 'time', 'name', 'author')
    fields = [('name', 'date', 'time'), 'author']
    inlines = [PollVariantsInline]
