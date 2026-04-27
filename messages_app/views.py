from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Message


@login_required
def inbox(request):
    messages = Message.objects.filter(
        receiver=request.user,
        message_type='sent'
    ).order_by('-timestamp')

    unread_count = Message.objects.filter(
        receiver=request.user,
        message_type='sent',
        read_status=False
    ).count()

    return render(request, 'messages_app/inbox.html', {
        'messages': messages,
        'unread_count': unread_count
    })


@login_required
def sent_messages(request):
    messages = Message.objects.filter(
        sender=request.user,
        message_type='sent'
    ).order_by('-timestamp')

    return render(request, 'messages_app/sent.html', {
        'messages': messages
    })


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.user != message.sender and request.user != message.receiver:
        return redirect('inbox')

    if request.user == message.receiver:
        message.read_status = True
        message.save()

    return render(request, 'messages_app/view.html', {
        'message': message
    })


@login_required
def compose_message(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        receiver_id = request.POST.get('recipient')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('body', '').strip()
        status = request.POST.get('status', 'sent')

        if not receiver_id or not content:
            return render(request, 'messages_app/compose.html', {
                'users': users,
                'error': 'Recipient and message content are required.'
            })

        receiver = get_object_or_404(User, id=receiver_id)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            content=content,
            message_type=status,
            status=status
        )

        if status == 'draft':
            return redirect('drafts')

        return redirect('sent_messages')

    return render(request, 'messages_app/compose.html', {
        'users': users
    })


@login_required
def drafts(request):
    messages = Message.objects.filter(
        sender=request.user,
        message_type='draft'
    ).order_by('-timestamp')

    return render(request, 'messages_app/drafts.html', {
        'messages': messages
    })


@login_required
def edit_draft(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user,
        message_type='draft'
    )

    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        receiver_id = request.POST.get('recipient')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('body', '').strip()
        status = request.POST.get('status', 'sent')

        if not receiver_id or not content:
            return render(request, 'messages_app/edit.html', {
                'message': message,
                'users': users,
                'error': 'Recipient and message content are required.'
            })

        receiver = get_object_or_404(User, id=receiver_id)

        message.receiver = receiver
        message.subject = subject
        message.content = content
        message.message_type = status
        message.status = status
        message.timestamp = timezone.now()
        message.save()

        if status == 'draft':
            return redirect('drafts')

        return redirect('sent_messages')

    return render(request, 'messages_app/edit.html', {
        'message': message,
        'users': users
    })


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender == request.user or message.receiver == request.user:
        message.delete()

    return redirect(request.META.get('HTTP_REFERER', 'inbox'))