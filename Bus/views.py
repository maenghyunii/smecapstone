from django.shortcuts import render, redirect
from .models import Bus
from django.views.decorators.http import require_POST

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
    # 수원으로 가는 버스 예약 페이지를 렌더링합니다.
    return render(request, 'Bus/toSuwon.html')

def toSeoul(request):
    # 서울로 가는 버스 예약 페이지를 렌더링합니다.
    return render(request, 'Bus/toSeoul.html')