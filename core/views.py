from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        profile_object = Profile.objects.get(user=user_object)
        ctx = {'profile_object': profile_object}
        return render(request, 'core/base.html', ctx)
    else:
        return render(request, 'core/base.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect("settings")
        else:
            messages.info(request, "Password not matching")
            return redirect('signup')
    else:
        return render(request, 'core/signup.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('signin')
        else:
            return render(request, 'core/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    profile_object = Profile.objects.get(user=request.user)
    ctx = {'profile_object': profile_object}

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = profile_object.profile_img
            about = request.POST['about']

            profile_object.profile_img = image
            profile_object.about = about
            profile_object.save()
            return redirect('/')
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            about = request.POST['about']

            profile_object.profile_img = image
            profile_object.about = about
            profile_object.save()
            return redirect('/')

    return render(request, 'core/settings.html', ctx)

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    profile_object = Profile.objects.get(user=user_object)
    ctx = {'user_object': user_object, 'profile_object': profile_object}
    return render(request, 'core/profile.html', ctx)