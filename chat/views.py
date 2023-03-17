from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Chat,CustomUser
from django.template import loader
from django.http import HttpResponse,JsonResponse

# Create your views here.

@login_required
def index(request,pk=None):
    user = request.user
    active_chat = None
    if pk:
        other_user = CustomUser.objects.get(pk=pk)
        chat = Chat.objects.filter(Q(Q(first_user=other_user) & Q(second_user=user)) | Q(Q(first_user=user) & Q(second_user=other_user)))
        if chat.exists():
            chat = chat.first()
        else:
            chat = Chat.objects.create(first_user=other_user,second_user=user)
        active_chat=chat.pk
    
    chats = Chat.objects.filter(Q(first_user=user) | Q(second_user=user))

    if not active_chat:
        if chats.exists():
            active_chat = chats[0].pk
    context = {
        'chats':chats,
        'sender':user,
        'active_chat':active_chat,
    }
    print(context)
    return render(request,'chat/index.html',context)

@login_required
def get_messages(request):
    pk = int(request.GET.get('id'))
    chat = Chat.objects.get(pk=pk)
    template = loader.get_template('chat/history.html')
    context = {'chat':chat, 'user':request.user}
    rendered_html = template.render(context)
    return HttpResponse(rendered_html)    
@login_required
def get_chat(request):
    pk = int(request.GET.get('id'))
    chat = Chat.objects.get(pk=pk)
    user = request.user
    other_user = chat.first_user if user==chat.second_user else chat.second_user
    data = {'fullname':str(other_user)}
    
    return JsonResponse(data)



def get_users(request):
    q = request.GET.get('q')
    user = request.user
    print('USer-:',user)
    users = [
        {
            'fullname':str(u),
            'id':u.id
        }
        for u in CustomUser.objects.exclude(pk=user.id).filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q))
    ]
    return JsonResponse({'users':users})
    # messages = [
    #     {
    #         'message':m.text,
    #         'sender_id':m.sender.id,
    #         'created':m.created
        
    #     }
    #     for m in chat.messages.all()
    # ]
    # return JsonResponse({'messages':messages})