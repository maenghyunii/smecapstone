from django.shortcuts import render, redirect, get_object_or_404
from .models import Bus, Schedule, Seat
from .forms import ReservationForm
from django.views.decorators.http import require_POST
import datetime
from datetime import date, timedelta


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
    dates = [date.today() + timedelta(days=i) for i in range(8) if (date.today() + timedelta(days=i)).weekday() < 5]

    context = {
        'dates': dates,
    }
    return render(request, 'Bus/toSuwon.html', context)

def toSeoul(request):
    dates = [date.today() + timedelta(days=i) for i in range(8) if (date.today() + timedelta(days=i)).weekday() < 5]

    context = {
        'dates': dates,
    }
    return render(request, 'Bus/toSeoul.html', context)