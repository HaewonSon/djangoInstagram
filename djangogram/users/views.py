from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm

def main(request):
    # get 방식이라면
    if request.method == 'GET':
        return render(request, 'users/main.html')

    # post 방식이라면
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('posts:index')) # 로그인 성공시 posts 앱 리다이렉트
        else :
            return render(request, 'users/main.html') # 로그인 실패시 메인페이지

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()

        return render(request, 'users/signup.html',{'form':form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid(): # 유효성검사
            form.save() # 저장

            username = form.cleaned_data['username'] # cleaned_data에 저장된 값
            password = form.cleaned_data['password']

            # 자동으로 로그인 : 위의 코드와 동일

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('posts:index'))  # 로그인 성공시 posts 앱 리다이렉트

        return render(request, 'users/main.html')  # 로그인 실패시 메인페이지

