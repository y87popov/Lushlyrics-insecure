from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm  # Import Django's built-in user creation form
from django.contrib.auth.forms import UserCreationForm  # Import Django's built-in user creation form
from django.contrib import messages


# import cardupdate

class RestrictedView(LoginRequiredMixin, TemplateView):
    template_name = 'restricted_page.html'
    login_url = '/login/'  # Redirect to the login page if not logged in
    redirect_field_name = 'next'  # Redirect back to the original page after login

class RestrictAnonymousAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [reverse('login'), reverse('signup')]  # Add public URLs here
        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect('login')
        return self.get_response(request)

@login_required(login_url='/login/')
def restricted_view(request):
    return render(request, 'restricted_page.html')

f = open('card.json', 'r')
CONTAINER = json.load(f)

def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})



def playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})




def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('default')  # Make sure to redirect to the correct home page or default view
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        print("Received POST request")  # Debug line
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug line
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("User authenticated successfully")  # Debug line
                login(request, user)
                return redirect('default')  # Redirect to the home page
            else:
                print("User authentication failed after signup")  # Debug line
                messages.error(request, 'Unable to authenticate user after signup.')
        else:
            print("Form is not valid:", form.errors)  # Debug line
            messages.error(request, 'There was an error creating your account. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})



