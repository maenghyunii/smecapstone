from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomUserCreationForm
from django.urls import reverse
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from Bus.models import Reservation
from django.contrib import messages

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

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')  # 로그인 성공 시 리다이렉트할 페이지
            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "로그인 실패")
        # 오류 발생 시 같은 페이지에 메시지와 함께 리다이렉트
        return redirect('login')  # 'login'은 로그인 페이지의 URL 이름입니다.
    else:
        return render(request, 'user/login.html')

# 이메일 재발송 함수
def resend_activation_email(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        send_activation_email(user, request)
        return HttpResponse("Activation email has been resent. Please check your email.")
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")

# 활성화 이메일 전송 함수
def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = "{0}activate/{1}/{2}/".format(request.build_absolute_uri('/'), uid, token)
    subject = 'Activate your account'
    message = 'Please click on the following link to activate your account: {0}'.format(activation_link)
    email_from = 'your_email@example.com'
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
        # 인증 백엔드 명시
        user.backend = 'user.authentication.EmailBackend'
        login(request, user, backend=user.backend)  # 사용자를 로그인 상태로 만듭니다.
        return redirect('home')  # 'home'은 프로젝트에 설정된 홈 페이지의 URL 이름입니다.
    else:
        # 활성화 링크가 유효하지 않을 때, 이메일 재발송 옵션을 제공
        if user:  # user 객체가 존재하면
            context = {'user_id': user.pk}
            return render(request, 'user/activation_invalid.html', context)
        else:
            return HttpResponse('Activation link is invalid!')
    
@login_required
def mypage(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    context = {
        'user': user,
        'reservations': reservations,
    }
    return render(request, 'user/mypage.html', context)