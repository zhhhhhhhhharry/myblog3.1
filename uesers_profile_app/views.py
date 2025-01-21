from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .form import UserLoginForm, UserRegisterForm
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                next_page = request.GET.get('next', 'article:article_all')
                return redirect(next_page)
            else:
                messages.error(request, "账号或密码输入有误，请重新输入！")
        else:
            messages.error(request, "请输入合法的账号和密码！")

        return render(request, 'user_login.html', {'form': user_login_form})

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'user_login.html', context)



def user_logout(request):
    logout(request)
    return redirect("article:article_all")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():

            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()

            login(request, new_user)
            messages.success(request, "注册成功，欢迎来到博客！")
            return redirect("article:article_all")
        else:
            messages.error(request, "注册数据输入有误，请检查后重新提交。")
            return render(request, 'user_register.html', {'form': user_register_form})

    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'user_register.html', context)


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user
    return render(request, 'user_profile.html', {
        'user': user,
        'profile': profile,
    })
#def footer()


