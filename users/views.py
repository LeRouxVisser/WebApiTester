from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} your account has now successfully been created. You will now be able to log into the site!')
            return redirect('WebApp-login')
        else:
            print('hello')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

# def profile(request):
#     return render(request, 'users/home.html')