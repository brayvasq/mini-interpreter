from django.urls import path
from . import views

urlpatterns = [
    path('sentences',views.SentenceListCreate.as_view(),name="sentences-all"),
    path('sentences/<int:pk>/', views.SentenceDetailView.as_view(), name="songs-detail"),
    path('auth/login/', views.LoginView.as_view(), name="auth-login"),
    path('auth/register/', views.RegisterUsers.as_view(), name="auth-register"),
    path('auth/check/', views.UserCheck.as_view(), name="auth-check"),
    path('users',views.UserList.as_view(),name="users-all"),
    path('users/<int:pk>',views.UserDelete.as_view(),name="users-delete"),
]