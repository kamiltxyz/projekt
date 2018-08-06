from django.urls import path
from django.contrib.auth import views as auth_views

from . import  views


urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('new_project/', views.new_project, name='new_project'),
    path('projects/', views.projects_list, name='projects_list'),
    path('project/<slug:project_slug>', views.project_details, name='project_details'),

    # auth views
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
