from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.urls import reverse
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 사용자를 비활성화 상태로 설정
            user.save()
            send_activation_email(user, request)  # 활성화 이메일 전송
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    # 이메일 내의 링크 형식을 조정해야 할 수 있습니다. 예제에서는 간단히 표현했습니다.
    activation_link = "{0}/activate/{1}/{2}/".format(request.build_absolute_uri('/'), uid, token)

    subject = 'Activate your account'
    message = 'Hi, please click the link to activate your account: {0}'.format(activation_link)
    email_from = 'note0315note@gmail.com'
    recipient_list = [user.email,]
    send_mail(subject, message, email_from, recipient_list)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # 사용자를 로그인 상태로 만듭니다.
        return redirect('home')  # 'home'은 프로젝트에 설정된 홈 페이지의 URL 이름입니다.
    else:
        return HttpResponse('Activation link is invalid!')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')  # 로그인 성공 시 리다이렉트할 페이지
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid login details.")
    else:
        return render(request, 'user/login.html')