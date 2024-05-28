from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import CustomUserCreationForm, BusRequestForm, LostItemForm, ViolationReportForm, FreeBoardPostForm
from django.urls import reverse
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import NoShow  # 수정: User 모델 중복 제거
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from Bus.models import Reservation, LostItem, ViolationReport, FreeBoardPost, BusRequest
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()  # 동적으로 사용자 모델 가져오기

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
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=user.backend)  # 사용자를 로그인 상태로 만듭니다.
        return redirect('home')  # 'home'은 프로젝트에 설정된 홈 페이지의 URL 이름입니다.
    else:
        # 활성화 링크가 유효하지 않을 때, 이메일 재발송 옵션을 제공
        if user:  # user 객체가 존재하면
            context = {'user_id': user.pk}
            return render(request, 'user/activation_invalid.html', context)
        else:
            return HttpResponse('Activation link is invalid!')

def injareport(request):
    if request.method == 'POST':
        if 'lost_item_submit' in request.POST:
            lost_item_form = LostItemForm(request.POST)
            if lost_item_form.is_valid():
                lost_item_form.save()
                return redirect('injareport')
        elif 'report_submit' in request.POST:
            report_form = ViolationReportForm(request.POST)
            if report_form.is_valid():
                report_form.save()
                return redirect('injareport')
        elif 'post_submit' in request.POST:
            post_form = FreeBoardPostForm(request.POST)
            if post_form.is_valid():
                post_form.save()
                return redirect('injareport')
    else:
        lost_item_form = LostItemForm()
        report_form = ViolationReportForm()
        post_form = FreeBoardPostForm()

    lost_items = LostItem.objects.all()
    reports = ViolationReport.objects.all()
    posts = FreeBoardPost.objects.all()
    context = {
        'lost_items': lost_items,
        'reports': reports,
        'posts': posts,
        'lost_item_form': lost_item_form,
        'report_form': report_form,
        'post_form': post_form,
    }
    return render(request, 'Bus/board.html', context)

@require_POST
def add_lost_item(request):
    lost_item_form = LostItemForm(request.POST)
    if lost_item_form.is_valid():
        lost_item_form.save()
    return redirect('injareport')

@require_POST
def add_report(request):
    report_form = ViolationReportForm(request.POST)
    if report_form.is_valid():
        report_form.save()
    return redirect('injareport')

@require_POST
def add_post(request):
    post_form = FreeBoardPostForm(request.POST)
    if post_form.is_valid():
        post_form.save()
    return redirect('injareport')

@require_POST
def delete_lost_item(request, item_id):
    lost_item = get_object_or_404(LostItem, id=item_id)
    lost_item.delete()
    return redirect('injareport')

@require_POST
def delete_report(request, report_id):
    report = get_object_or_404(ViolationReport, id=report_id)
    report.delete()
    return redirect('injareport')

@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(FreeBoardPost, id=post_id)
    post.delete()
    return redirect('injareport')


def submit_bus_request(request):
    dates = [date.today() + timedelta(days=i) for i in range(4) if (date.today() + timedelta(days=i)).weekday() < 5]
    
    if request.method == 'POST':
        form = BusRequestForm(request.POST)
        if form.is_valid():
            bus_request = BusRequest(
                #user=request.user,
                destination=form.cleaned_data['destination'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                reason=form.cleaned_data['reason']
            )
            bus_request.save()
            return render(request, 'Bus/success_popup.html', {'message': "증원 요청이 완료되었습니다!"})
        else:
            print("Form is not valid")
            print(form.errors)  # 폼 에러 출력
    else:
        form = BusRequestForm()

    return render(request, 'Bus/board.html', {'form': form, 'dates': dates})

@login_required
def mypage(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    context = {
        'user': user,
        'reservations': reservations,
    }
    return render(request, 'user/mypage.html', context)


def user_logout(request):
    logout(request)
    return redirect('login') 

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def manage_no_show(request):
    no_shows = NoShow.objects.all()
    return render(request, 'user/manage_no_show.html', {'no_shows': no_shows})

@staff_member_required
def admin_bus_requests(request):
    # 관리자가 볼 수 있는 페이지에 이전에 제출된 모든 증원 요청을 표시
    requests = BusRequest.objects.all()
    return render(request, 'admin_bus_requests.html', {'requests': requests})
