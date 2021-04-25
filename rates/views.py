from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def index(request):
    return HttpResponse("<p>Hello world, you're at the rates index.</p>"
                        "<p><a href=\"/accounts/logout\">Log out</a></p>")
