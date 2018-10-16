from django.contrib import admin

from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ['age', 'type']


admin.site.register(models.User)
admin.site.register(models.Article)