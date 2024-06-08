from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Schedule, Seat
from .forms import ReservationForm
from django.views.decorators.http import require_POST
import datetime
from datetime import date, timedelta
from django.http import HttpResponse


def home(request):
    return render(request, 'Bus/home.html')


@require_POST
def route_selection(request):
    route_direction = request.POST.get('route_direction')
    if route_direction == 'toSuwon':
        return redirect('toSuwon')
    else:
        return redirect('toSeoul')

def toSuwon(request):
    dates = [date.today() + timedelta(days=i) for i in range(4) if (date.today() + timedelta(days=i)).weekday() < 5]

    context = {
        'dates': dates,
    }
    return render(request, 'Bus/toSuwon.html', context)

def toSeoul(request):
    dates = [date.today() + timedelta(days=i) for i in range(4) if (date.today() + timedelta(days=i)).weekday() < 5]

    context = {
        'dates': dates,
    }
    return render(request, 'Bus/toSeoul.html', context)

def board(request):
    return render(request, 'Bus/board.html')

def reservation(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    # 필터링
    seats = Seat.objects.filter(schedule__departure_date=date, schedule__departure_time=time)
    context = {
        'date': date,
        'time': time,
        'seats': seats,
    }
    return render(request, 'Bus/reservation.html', context)

from django.http import JsonResponse

def check_reservation(request, seat_number):
  try:
    seat = Seat.objects.get(seat_number=seat_number)
    is_reserved = seat.is_reserved
  except Seat.DoesNotExist:
    is_reserved = False
  return JsonResponse({'is_reserved': is_reserved})

def notice(request):
    return render(request, 'Bus/notice.html')  # 공지사항 템플릿 렌더링
from django.shortcuts import render

# 정류장 지도 페이지 뷰
def seoulbus(request):
    return render(request, 'Bus/seoulbus.html')