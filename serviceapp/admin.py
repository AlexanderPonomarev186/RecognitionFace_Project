from django.contrib import admin
from serviceapp.models import *


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "image", "isactive")
    list_display_links = ("pk", "name", "image", "isactive")
    readonly_fields = ('pk',)
