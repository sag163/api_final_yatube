from django.contrib import admin

# Register your models here.
from .models import Post, Follow, Group

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Follow)
