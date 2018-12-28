from django.urls import path
from . import views

urlpatterns = [
    path('sentences',views.SentenceListCreate.as_view(),name="sentences-all"), # Url para listar todas las sentencias
    path('sentences/<int:pk>', views.SentenceDetailView.as_view(), name="songs-detail"), # Url para listar los detalles de una sentencia
    path('auth/login/', views.LoginView.as_view(), name="auth-login"), # Url para loguearse en la app
    path('auth/register/', views.RegisterUsers.as_view(), name="auth-register"), # Url para registrar usuarios
    path('auth/check/', views.UserCheck.as_view(), name="auth-check"), # Url para verificar el usuario y el rol
    path('users',views.UserList.as_view(),name="users-all"), # Url para listar todos los usuarios
    path('users/<int:pk>',views.UserDelete.as_view(),name="users-delete"), # Url para eliminar un usuario
]