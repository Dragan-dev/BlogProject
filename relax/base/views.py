from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# User login/out/register section


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, password=password, username=username)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR  password Incorect")

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, "An error ocurred due the registration ! Please use at least one upper letter and least one number")
    return render(request, 'login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q))

    topics = Topic.objects.all()[:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,
        'room_messages': room_messages,

    }
    return render(request, 'home.html', context)


def room(request, pk):

    chased_room = Room.objects.get(id=pk)
    room_messages = chased_room.message_set.all().order_by('-created')
    participants = chased_room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=chased_room,
            body=request.POST.get('body')
        )
        chased_room.participants.add(request.user)
        return redirect('room', pk=chased_room.id)
    context = {

        'room': chased_room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'room.html', context)

# Room CRUD section


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()

    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics

    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # Part of code which check if 'topic_name' is new or not
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # and return or create new and return it
        Room.objects.create(
            topic=topic,
            name=request.POST.get('name'),
            host=request.user,
            description=request.POST.get('description')

        )

        return redirect('home')

    context = {
        'form': form,
        'topics': topics,
    }
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You have no permission for editing this post!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {
        'form': form,
        'topics': topics,
        'room': room,

    }
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {
        'obj': room
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete message!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {
        'message': message
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {
        'form': form,

    }
    return render(request, 'update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics,

    }

    return render(request, 'topics.html', context)



def activityPage(request):
    room_messages = Message.objects.all()
    context = {
        'room_messages':room_messages,
    }
    return render(request,'activity.html', context)