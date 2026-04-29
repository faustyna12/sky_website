from django.shortcuts import render
from django.contrib.auth.models import User

def reports_dashboard(request):
    total_users = User.objects.count()
    context = {
        'total_users': total_users,
    }
    return render(request, 'reports_app/reports.html', context)