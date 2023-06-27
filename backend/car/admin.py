from django.contrib import admin

from .models import Car, Comment, UnderComment

admin.site.register(Car)
admin.site.register(Comment)
admin.site.register(UnderComment)
