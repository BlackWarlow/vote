from django.contrib import admin

# Register your models here.
from vote.models import Pool, Pool_variant


class PoolVariantsInline(admin.TabularInline):
    model = Pool_variant
    extra = 0


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'name', 'author')
    list_filter = ('id', 'date', 'time', 'name', 'author')
    fields = [('name', 'date', 'time'), 'author']
    inlines = [PoolVariantsInline]
