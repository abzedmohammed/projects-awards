from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def single_project(request):
    return render(request, 'awards.html')