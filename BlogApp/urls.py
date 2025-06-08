"""
URL configuration for BlogApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add_blog/', views.add_blog_post, name='add_blog'),
    # path('',views.home,name='home'),
    path('',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('home',views.home,name='home'),
    path('likecount/<int:blog_id>/', views.likecount, name='likecount'),
    path('logout',views.logout,name='logout'),
    path('show_post/<int:blog_id>/', views.show_post, name='show_post'),
    path('add_comment/<int:blog_id>/',views.add_comment,name='add_comment'),
    path('profile',views.profile,name='profile'),
    path('bookmark/<int:blog_id>/',views.bookmark,name='bookmark'),
    path('show_bookmarks',views.show_bookmarks,name='show_bookmarks'),
    path('remove_bookmark/<int:blog_id>/',views.remove_bookmark,name='remove_bookmark'),


]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


