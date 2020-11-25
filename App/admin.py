from django.contrib import admin
from .models import profile,Post,Comments

# Register your models here.

admin.site.register(profile)
# admin.site.register(Post)

@admin.register(Post)
class person(admin.ModelAdmin):
    list_display = ['id','user','postText','postImage']

admin.site.register(Comments)
