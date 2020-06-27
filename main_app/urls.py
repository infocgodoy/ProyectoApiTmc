from django.urls import path
from .views import home, resultado

urlpatterns = [
    path("", home, name="home"),
    path("resultado/", resultado, name="resultado"),
]