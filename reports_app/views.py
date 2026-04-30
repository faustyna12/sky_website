from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from teams_app.models import Team
from organisation_app.models import Department
from messages_app.models import Message
from django.db.models import Count

def reports_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('dashboard_home')
    
    search = request.GET.get('search', '')
    user_search = request.GET.get('user_search', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    total_users = User.objects.count()
    total_teams = Team.objects.count()
    total_departments = Department.objects.count()
    total_messages = Message.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Most active users (most messages sent)
    most_active_users = User.objects.annotate(
        messages_sent=Count('sent_messages')
    ).order_by('-messages_sent')[:5]

    # Departments breakdown
    departments = Department.objects.all()

    if search:
        all_teams = Team.objects.filter(name__icontains=search)
    else:
        all_teams = Team.objects.all()

    if user_search:
        all_users = User.objects.filter(username__icontains=user_search)
    else:
        all_users = User.objects.all()

    # Date filter
    if date_from:
        all_users = all_users.filter(date_joined__gte=date_from)
    if date_to:
        all_users = all_users.filter(date_joined__lte=date_to)
    
    context = {
        'total_users': total_users,
        'total_teams': total_teams,
        'total_departments': total_departments,
        'total_messages': total_messages,
        'recent_users': recent_users,
        'most_active_users': most_active_users,
        'departments': departments,
        'all_teams': all_teams,
        'all_users': all_users,
        'search': search,
        'user_search': user_search,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'reports_app/reports.html', context)