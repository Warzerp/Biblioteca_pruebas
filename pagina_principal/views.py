from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UsuarioForm


def principal(request):
    return render(request, "pagina_principal/principal.html")

def catalogo(request):
    return render(request, "catalogo/catalogo.html")

def reservar(request):
    return render(request, "reservar/reservar.html")

def sesion(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(request, "inicio_sesion/sesion.html",
                    {"form": form})
    return render(
            request, "inicio_sesion/sesion.html",
            {"form": form},
        )