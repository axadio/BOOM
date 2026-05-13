from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q, Count
from .models import Room, Topic, Message, User
from .forms import RoomForm, MyUserCreationForm, UserForm

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':                            
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Password is incorrect')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        name__icontains=q
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    # Faqat user participants bo'lgan roomlardagi habarlarni ko'rsatish
    if request.user.is_authenticated:
        recent_messages = Message.objects.filter(room__participants=request.user).order_by('-created')[:5]
    else:
        recent_messages = Message.objects.none()

    if request.method == 'GET':
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        rooms = Room.objects.filter(
            name__istartswith=q
            )
        

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'recent_messages': recent_messages
        }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = Message.objects.filter(room__id=pk).order_by('created')
    participants = room.participants.all()

    if request.method == 'POST' and request.POST.get('body') != '':
        if not request.user.is_authenticated:
            return redirect('login')
        comment = Message(user=request.user, room=room, body=request.POST.get('body'))
        comment.save()
        room.participants.add(request.user)
        return redirect('room', pk)


    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = request.user
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):
    action = 'update'
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form, 'action': action}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.id)
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    recent_messages = user.message_set.all().order_by('-updated', '-created')[:5]

    context = {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'recent_messages': recent_messages,
        }
    return render(request, 'base/user_profile.html', context)

def topicsPage(request):
    topics = Topic.objects.annotate(room_count=Count('room')).order_by('-room_count')

    if request.method == 'GET':
        q = request.GET.get('q') if request.GET.get('q') != None else ''

        topics = Topic.objects.filter(name__istartswith=q)

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def get_room_messages(request, pk):
    """API endpoint - yangi xabarlarni JSON formatida qaytaradi"""
    try:
        room = Room.objects.get(id=pk)
        room_messages = Message.objects.filter(room__id=pk).order_by('created')
        
        messages_data = []
        for message in room_messages:
            messages_data.append({
                'id': message.id,
                'username': message.user.username,
                'user_id': message.user.id,
                'body': message.body,
                'created': message.created.isoformat(),
                'user_is_current': message.user.id == request.user.id,
                'avatar_url': message.user.avatar.url if message.user.avatar else '/static/default-avatar.png'
            })
        
        return JsonResponse({
            'success': True,
            'messages': messages_data
        })
    except Room.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not found'})
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def activityPage(request):
    if request.user.is_authenticated:
        recent_messages = Message.objects.filter(room__participants=request.user).order_by('-created')[:5]
    else:
        recent_messages = Message.objects.none()
    context = {'recent_messages': recent_messages}
    return render(request, 'base/activity.html', context)



