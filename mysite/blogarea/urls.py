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
from .views import BlogHome, ArticleDetailView, AddPostView, ShowProfileView, UpdatePostView,  CategoriesView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", BlogHome.as_view(), name="blogarea"),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name="ArticleDetailView"),
    path('writeYourBlog/',AddPostView.as_view(),name="writeYourBlog"),
    path('article/updateBlog/<int:pk>',views.UpdatePostView,name="updateBlog"),
    path('article/deleteBlog/<int:pk>', views.deleteBlog, name="deleteBlog"),
    path('category/<str:cats>',views.CategoryView,name='category'),
    path('likes/<int:pk>',views.LikeView,name='like_post'),
    path('show_profile_page/<int:pk>/',ShowProfileView.as_view(),name="show_profile_page"),
    path('load-more/',views.load_more,name="load-more"),
    path('filtered_load_more/',views.filtered_load_more,name="filtered_load_more"),
    path('submit_comment/',views.submit_comment,name="submit_comment"),
    path('answer/',views.answer,name="answer"),
    path('categories/',CategoriesView.as_view(),name="categories_list"),
    path('categories/<str:tag>/',views.CategoryView,name="categories_detail"),
    path('search/',views.search,name="search"),
    path('searchresult/',views.searchresult,name="searchresult"),
    path('random-post/',views.random_post,name="random-post"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)