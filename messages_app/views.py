from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone   

@login_required
def inbox(request):
    messages = Message.objects.filter(
        receiver=request.user,).order_by(
            '-timestamp') 
    unread_count = Message.objects.filter(
        receiver=request.user, read_status=False).count()
    
    return render(request, 'messages_app/inbox.html', {'messages': messages, 'unread_count': unread_count})   


@login_required
def sent_messages(request):     
    messages = Message.objects.filter(
        sender=request.user, message_type='sent').order_by('-timestamp')
    return render(request, 'messages_app/sent_messages.html', {'messages': messages})        
           

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.sender and request.user not in message.receiver.all():
        return redirect('inbox')
    if request.user in message.receiver.all() and not message.read_status:
        message.read_status = True
        message.save()
    return render(request, 'messages_app/view_message.html', {'message': message})


@login_required
def compose_message(request):

    initial_receivers = request.GET.get('to')
    initial_subject = request.GET.get('subject', '')

    if request.method == 'POST':
        receiver_ids = request.POST.getlist('receiver')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()
        status = request.POST.get('status', 'sent')

        receivers = User.objects.filter(id__in=receiver_ids)

        if status == 'sent' and (not receiver_ids or not content):
            return render(request, 'messages_app/compose_message.html', {
                'error': 'Recipients and message content are required.',
                'initial_subject': subject
            })

        message = Message.objects.create(
            sender=request.user,
            subject=subject,
            content=content,
            message_type=status
        )

        message.receiver.set(receivers)

        if status == 'draft':
            return redirect('drafts')

        return redirect('sent_messages')

    context = {
        'initial_subject': initial_subject
    }

    if initial_receivers:
        context['initial_receivers'] = [int(i) for i in initial_receivers.split(',')]

    return render(request, 'messages_app/compose_message.html', context)

@login_required
def drafts(request):
    messages = Message.objects.filter(
        sender=request.user, message_type='draft').order_by('-timestamp')
    return render(request, 'messages_app/drafts.html', {'messages': messages})

@login_required
def edit_draft(request, message_id):    
    message = get_object_or_404(
        Message, id=message_id, sender=request.user, message_type='draft')
    
    if request.method == 'POST':
        receiver_ids = request.POST.getlist('receiver')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()

        receivers = User.objects.filter(id__in=receiver_ids)

        message.receiver.set(receivers)
        message.subject = subject
        message.content = content
        message.message_type = 'sent'
        message.timestamp = timezone.now()
        message.save()

        return redirect('sent_messages')

    return render(request, 'messages_app/edit_draft.html', {'message': message})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender == request.user or message.receiver == request.user:
        message.delete()

    return redirect(request.META.get("HTTP_REFERER", "inbox"))
    
