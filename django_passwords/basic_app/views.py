from django.shortcuts import render
import basic_app

from basic_app.forms import UserFrom
from basic_app.forms import UserProfileInfoForm 
from django.urls import reverse
from django.contrib.auth.decorators import login_required;
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

def index(request):
    return render(request,'basic_app/index.html');

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))  ;



def register (request):
    registered=False;
    if request.method=="POST":
        user_form=UserFrom(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST);
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password);
            user.save();
            profile=profile_form.save(commit=False);
            profile.user=user;
            if 'profile_pic' in request.FILES:
                profile.profile_pic= request.FILES['profile_pic']
            profile.save() 
            registered=True;
    else:
        user_form=UserFrom();
        profile_form=UserProfileInfoForm();        

    return    render(request,'basic_app/registration.html',
    {'user_form':user_form,
     'profile_form':profile_form,
     'registered':registered})    


def user_login(request):
   
    if request.method=='POST':
        username=request.POST.get('username');
        password=request.POST.get('password');
        user=authenticate(username=username,password=password);
        print(user)

        if user:
            if user.is_active:
                login(request,user)
                return  render(request,'basic_app/base.html')
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')  

        else:
            print('someone tried to login and failed')
            return HttpResponse('invalid login response');

    else:
        return render(request,'basic_app/login.html',{}) 



    


# Create your views here.
