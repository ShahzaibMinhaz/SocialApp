from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('profile/<int:id>',views.profile,name='profile'),
    path('',views.home,name='home'),
    path('logout',views.logoutuser,name='logout'),
    path('MyPost',views.Mypost,name='mypost'),
    path('comments',views.comments,name='comments')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)