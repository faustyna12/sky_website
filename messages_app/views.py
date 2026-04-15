from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone   

# Create your views here.
