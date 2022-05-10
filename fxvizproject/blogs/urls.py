"""fxvizproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

from .views import *

app_name="blogs"
urlpatterns = [
    path('', ArticleListView.as_view(), name="article-list")
    ,path('create/', ArticleCreateView.as_view(), name="article-create")
    ,path('<int:id>/', ArticleDetailView.as_view(), name="article-detail")
    ,path('<int:id>/delete', ArticleDeleteView.as_view(), name="article-delete")
    ,path('<int:id>/update', ArticleUpdateView.as_view(), name="article-update")
    ]