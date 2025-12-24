from django.urls import path
from . import views

app_name = 'authentification'
urlpatterns = [
path('admin-login/', views.admin_login_view, name='admin-login'),
# path('Super-admin-login/', views.super_admin_login_view, name='Super-login'),
path("logout/", views.logout_view, name="logout"),
]
