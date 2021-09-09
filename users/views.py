from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    """
        Function is used to store new users credentials in DB after registration.
        Function will also send back a message if registration was successful.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} your account has now successfully been created. You will now be able to log into the site!')
            return redirect('WebApp-login')
        else:
            print('register form not valid')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})