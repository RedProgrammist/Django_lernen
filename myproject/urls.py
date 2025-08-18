"""
URL configuration for myproject project.

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
from django.contrib import admin
from django.urls import *
from rest_framework.routers import DefaultRouter

from myapp import views
from myapp.views import hello_world

router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world, name='hello_world'),
    path('', hello_world, name='home'),
    path('tasks/create/', views.task_create, name='create_task'),
    path('tasks/alltasks/', views.tasks_list, name='tasks_list'),
    path('tasks/tasks_byid/<int:id>/', views.tasks_byid, name='tasks_byid'),
    path('tasks/tasks_stat/', views.tasks_stat, name='tasks_stat'),
    path('tasks/create_list/', views.TaskListCreateView.as_view(), name='create_list'),
    path('tasks/g_u_d/<int:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name='g_u_t'),
    path('tasks/allsubtasks/', views.SubTaskListCreateView.as_view(), name='allsubtasks'),
    path('tasks/subg_u_d/<int:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(), name='subg_u_t'),
    path('category/', include(router.urls)),
]
