from django.contrib import admin
from .models import Post, Comment, ReplyComment, Category, Series, Tag

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Category)
admin.site.register(Series)
admin.site.register(Tag)
