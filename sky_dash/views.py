from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # This renders the index.html file inside the dashboard folder
    return render(request, 'sky_dash/sky_dash.html')