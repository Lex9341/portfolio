from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    # Projects
    path('projects/', views.projects, name='admin_projects'),
    path('projects/add/', views.project_add, name='admin_project_add'),
    path('projects/<int:pk>/edit/', views.project_edit, name='admin_project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='admin_project_delete'),

    # Skills
    path('skills/', views.skills, name='admin_skills'),
    path('skills/add/', views.skill_add, name='admin_skill_add'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='admin_skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='admin_skill_delete'),

    # Auth
    path('login/', views.login_view, name='adminpanel-login'),
    path('logout/', views.logout_view, name='adminpanel-logout'),
]