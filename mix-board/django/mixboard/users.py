from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.template import Template, Context
from mixboard.main import serveStatic, workingDir
from mixboard.models import UserProfile, Song

def login(request):
  username = request.POST['username']
  password = request.POST['password']

  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      auth_login(request, user)
      return HttpResponse('success')
    else:
      return HttpResponse('Account disabled.')
  else:
    return HttpResponse('Incorrect username or password.')

def logout(request):
  auth_logout(request)
  return HttpResponse()

def signup(request):
  return serveStatic(request, 'signup.html')

def register(request):
  username = request.POST['username']
  email    = request.POST['email']
  password = request.POST['password']

  if len(username) == 0:
    return HttpResponse('Please enter a name.')
  elif len(username) < 3:
    return HttpResponse('Name must contain at least 3 characters.')
  elif len(username) > 30:
    return HttpResponse('Name must contain 30 characters or fewer.')
  elif len(User.objects.filter(username=username)) != 0:
    return HttpResponse('Name already in use.')

  if len(email) == 0:
    return HttpResponse('Please enter an email address.')
  elif not '.' in email or not '@' in email:
    return HttpResponse('Please enter a valid email address.')

  if len(password) == 0:
    return HttpResponse('Please enter a password.')
  elif len(password) < 6:
    return HttpResponse('Password must contain at least 6 characters.')

  user = User.objects.create_user(username, email, password)
  user.save()

  authUser = authenticate(username=username, password=password)
  auth_login(request, authUser)

  return HttpResponse('success')

def list(request):
  f = open(workingDir + '/templates/list_users.html', 'r')
  users = User.objects.all()
  result = Template(f.read()).render(Context({'user': request.user, 'users': users}))
  return HttpResponse(result, content_type='text/html')

def profile(request, username):
  requestedUser = User.objects.get(username=username)
  profile       = UserProfile.objects.get(user=requestedUser)
  songs         = Song.objects.filter(owner=requestedUser).order_by('-vote_count')
  context = Context({'user': request.user,
                     'requestedUser': requestedUser,
                     'profile': profile,
                     'songs': songs})

  f = open(workingDir + '/templates/profile.html', 'r')
  result = Template(f.read()).render(context)
  return HttpResponse(result, content_type='text/html')
