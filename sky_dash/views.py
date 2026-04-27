from django.shortcuts import render

def dashboard_index(request):
    # This looks for the HTML file we're about to create
    return render(request, 'sky_dash/index.html')
