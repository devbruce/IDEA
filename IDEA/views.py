from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def interactive(request):
    return render(request, "IDEA_Interactive/home.html")

def simple(request):
    return render(request, "IDEA_Simple/home.html")