from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # This protects the page from unlogged-in users
def home(request):
    return render(request, 'login_app/login.html')
