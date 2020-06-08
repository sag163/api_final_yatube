from django.contrib import admin
from .models import Post, Follow, Group

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Follow)
