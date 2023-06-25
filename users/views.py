import os
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm, UserProfileForm
from .models import UserProfile


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"User Created {username}!")
            UserProfile(biography="", user=user).save()
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def redirect_login(request):
    return redirect("home")


@login_required
def update_profile(request):
    active_user = request.user

    try:
        profile = UserProfile.objects.get(user=active_user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=active_user)
        
    form = UserProfileForm(request.POST or None, request.FILES, instance=profile)
    
    if request.method == "POST":
        # deleting old uploaded image.
        if (
            profile.picture
            and os.path.exists(profile.picture.path)
            and os.path.basename(profile.picture.path) != "default.jpg"
        ):
            os.remove(profile.picture.path)

        # form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "users/update_profile.html", {"form": form, "profile": profile})

def profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__pk=user_id)
    
    return render(request, "users/profile.html", {"user_profile": user_profile})
