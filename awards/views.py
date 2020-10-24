from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http  import HttpResponse
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .forms import *
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.conf import settings 
from django.urls import reverse
from django.core.paginator import Paginator
from django.template import loader

def index(request):
    return render(request, 'index.html')

def single_project(request):
    paginator = Paginator('ratings', 6)
    page_number = request.GET.get('page')
    ratings_paginator = paginator.get_page(page_number)
    temlate = loader.get_template('awards.html')
    
    context = {
        'rates': ratings_paginator,
    }
    
    return HttpResponse(template.render(context, request))