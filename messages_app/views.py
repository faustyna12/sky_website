from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone   

@login_required
def inbox(request):
    messages = Message.objects.filter(
        receiver=request.user, message_type='sent').order_by(
            '-timestamp') #only show sent messages in inbox
    unread_count = Message.objects.filter(
        receiver=request.user, message_type='sent', read_status=False).count()
    
    return render(request, 'messages_app/inbox.html', {'messages': messages, 'unread_count': unread_count})   


@login_required
def sent_messages(request):     
    messages = Message.objects.filter(
        sender=request.user, message_type='sent').order_by('-timestamp')
    return render(request, 'messages_app/sent_messages.html', {'messages': messages})        
           

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user and message.sender != request.user:
        return redirect('inbox')
    if message.receiver == request.user and not message.read_status:
        message.read_status = True
        message.save()
    return render(request, 'messages_app/view_message.html', {'message': message})


@login_required
def compose_message(request):       

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()
        
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return render(request, 'messages_app/compose_message.html', {'error': 'Receiver not found.'})
        Message.objects.create(sender=request.user, receiver=receiver, subject=subject, content=content, message_type='sent')
        return redirect('sent_messages')
    return render(request, 'messages_app/compose_message.html')     


@login_required
def drafts(request):
    messages = Message.objects.filter(sender=request.user, message_type='draft').order_by('-timestamp')
    return render(request, 'messages_app/drafts.html', {'messages': messages})


@login_required
def edit_draft(request, message_id):    
    message = get_object_or_404(Message, id=message_id, sender=request.user, message_type='draft')
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return render(request, 'messages_app/edit_draft.html', {'message': message, 'error': 'Receiver not found.'})
        message.receiver = receiver
        message.subject = subject
        message.content = content
        message.message_type = 'sent'
        message.timestamp = timezone.now()
        message.save()
        return redirect('sent_messages')
    return render(request, 'messages_app/edit_draft.html', {'message': message})        

login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver == request.user or message.sender == request.user:
        message.delete()
    return redirect('inbox')
    
