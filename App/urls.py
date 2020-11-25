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
    path('addcomments/<int:id>',views.addcomments,name='addcomments'),
    path('delete_comment/<int:id>',views.delete_comment,name='delete_comment'),
    path('findothers',views.findothers,name='findothers'),
    path('friendrequest/<int:user_id>/<int:friends_id>',views.sendfriendrequset,name='friendrequest'),
    path('getfriendrequest',views.getfriendrequest,name='getfriendrequest')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)