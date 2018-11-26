## Django REST API

Creando el directorio.

```bash
mkdir django-rest-prj && cd django-rest-prj
```

Instalando `pipenv`

```bash
pip install --user pipenv
```

Creando estructura `pipenv`

```bash
pipenv --three
```

Instalando `django`, `django-rest-framework` y `ply`

```bash
pipenv install django djangorestframework ply
```

Activar entorno virtual

```bash
pipenv shell
```

Creando el proyecto

```bash
django-admin startproject project && cd project
```

Creando aplicación

```bash
django-admin startapp app_name
```

Añadiendo la app creada y `rest_framework` para que `django` las use.

```python
# ./project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # django rest framework
    'app', # aplicación creada
]
```

### Creando Modelo

```python
# app/models.py
from django.db import models

class Sentence(models.Model):
    # Código de entrada
    input_code = models.CharField(max_length=100)
    # Resultado arrojado por el parser
    output_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} => {}".format(self.input_code, self.output_code)
```



### Creando Serializers

creando el archivo `serializers.py`

```bash
touch serializers.py
```

creando el serializer para la clase `Sentence`

```python
# app/serializers.py
from rest_framework import serializers
from app.models import Sentence

class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name', 'email', 'message')
```

serializer para todos los campos del modelo

```python
class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
```

### Creando Views

```python
# app/views.py

from app.models import Sentence
from app.serializers import SenteneSerializer
from rest_framework import generics

class SentenceListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
```

`ListCreateAPIView` provee los métodos `GET` y `POST`, para sobrescribirlos se crean funciones.

```python
class SentenceListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    
    def list(self):
        pass
    def post(self):
        pass
```

### Añadiendo rutas

Añadir rutas globales

```python
# project/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]
```

Añadir rutas de la app

```python
# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/sentence/', views.SentenceListCreate.as_view() ),
]
```

### Registrando App en Admin

```python
# app/admin.py

from django.contrib import admin
from .models import Sentence

admin.site.register(Sentence)
```

### Auth con JWT

Instalando `JWT`

```bash
pipenv install djangorestframework-jwt
```

Añadir `JWT` a la configuración de las clases de autenticación

```python
# project/settings.py

REST_FRAMEWORK = {
    # ...
    
    # Authentication settings
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    
    #...
}
```

Añadir configuración `JWT`

```python
# project/settings.py
# ...

# JWT settings
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_AUTH_COOKIE': None,
}
# ...
```

Añadir configuración de las clases de permisos

```python
# project/settings.py

REST_FRAMEWORK = {
    # ...
    
    # Permission settings
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    
    #...
}
```

Importar módulos de `JWT`  y de permisos en `views.py` 

```python
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
```

Añadir `serializer` del token

```python
class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
```

Añadir vista de `login` para la autenticación mediante `JWT`

```python
class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,) # Esta linea añade permisos sobre la
    											 # Vista, en este caso permite el 
        										 # acceso a todos
    queryset = User.objects.all() # Objeto que será usado para realizar las 
    							  # Operaciones sobre el objeto

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
			# Se guarda el usuario en las sessiones de django rest
            login(request, user)
            serializer = TokenSerializer(data={
                # se genera el token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

```

Para indicarle a la vista que solo puede acceder usuarios autenticados se puede usar:

```python
permission_classes = (permissions.IsAuthenticated,)
```

### USER personalizado

Creando `user` personalizado añadiendo campos adicionales

```python
# app/models.py

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_coder = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
```

Usando el modelo para autenticación

```python
# project/settings.py
AUTH_USER_MODEL = 'app.User'
```

Reemplazar imports

```python
from django.contrib.auth.models import User
# Cambiar a
from django.contrib.auth import get_user_model
User = get_user_model()
```

### Configurando BD

#### Usando mysqlclient

Instalar driver mysql

```python
pipenv install mysqlclient
```

Configurar driver

```python
# app/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'interpreterdb',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': ''
    }
}
```

#### Usando mysql-connector

Instalar driver mysql

```bash
pipenv install mysql-connector
```

Configurar driver

```python
# app/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'HOST': 'localhost',
        'NAME': 'interpreterdb',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}
```

En muchos casos este driver saca error con nuevas versiones de django, para solucionar se debe hacer lo siguiente:

- descargar el archivo `base.py` de https://github.com/mysql/mysql-connector-python/blob/master/lib/mysql/connector/django/base.py
- pegar y reemplazar el archivo `base.py` descargado en `virtual_env_project\Lib\site-packages\mysql\connector\django`

### React App
Compilar react app
```bash
npm run dev
```

### Preview
![login](https://github.com/brayvasq/mini-interpreter/blob/master/project/frontend/static/images/login.PNG)
![users](https://github.com/brayvasq/mini-interpreter/blob/master/project/frontend/static/images/preview-user.PNG)
![code_1](https://github.com/brayvasq/mini-interpreter/blob/master/project/frontend/static/images/code-prev.PNG)
![code_2](https://github.com/brayvasq/mini-interpreter/blob/master/project/frontend/static/images/code-prev-1.PNG)

### Referencias

- [Django REST with React ](https://www.valentinog.com/blog/tutorial-api-django-rest-react/)
- [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/ply.html)
- [Let’s build an API with Django REST Framework — Part 2](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-part-2-cfb87e2c8a6c)
- [mysql-connector and django](https://bugs.mysql.com/bug.php?id=86105)
- [manager-isnt-available-user-has-been-swapped-for-pet-person](https://stackoverflow.com/questions/17873855/manager-isnt-available-user-has-been-swapped-for-pet-person)
- [roles-de-usuarios-en-django](https://es.stackoverflow.com/questions/930/roles-de-usuarios-en-django)

