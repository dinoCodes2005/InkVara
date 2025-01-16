"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from tkinter.font import names

from django.urls import path
from . import views
from .views import BlogHome, ArticleDetailView, AddPostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("blogarea/", views.blogarea, name="blogarea"),
    path("blogarea/", BlogHome.as_view(), name="blogarea"),
    path('home/', views.logout_user, name='logout'),
    path('article/<int:pk>',ArticleDetailView.as_view(),name="ArticleDetailView"),
    path('writeYourBlog/',AddPostView.as_view(),name="writeYourBlog"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
