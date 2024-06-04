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
    context = {
        'date': date,
        'time': time,
    }
    return render(request, 'Bus/reservation.html', context)