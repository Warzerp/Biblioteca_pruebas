from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "pagina_principal"


urlpatterns = [
    path("", views.principal, name="principal"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("reservar/", views.reservar, name="reservar"),
    path("inicio_sesion/", views.sesion, name="sesion"),
]