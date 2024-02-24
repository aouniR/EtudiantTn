from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db import models
from django.contrib.auth import get_user_model

@login_required
def chat(request, receiver_id):
    receiver = get_user_model().objects.get(pk=receiver_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'chat/chat.html', {'receiver': receiver, 'messages': messages})

@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = get_user_model().objects.get(pk=receiver_id)
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
    
    return redirect('chat:chat', receiver_id=receiver_id)
