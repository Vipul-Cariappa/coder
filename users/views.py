from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

# Create your views here.
def index(request):
    return render(request, 'demo.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"User Created {username}!")
            return redirect('users:index')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def redirect_login(request):
    return redirect('users:index')
