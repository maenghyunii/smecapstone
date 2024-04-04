from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Bus(models.Model):
    name = models.CharField(max_length=100)
    route_direction = models.CharField(max_length=50)  # "수원-서울", "서울-수원" 등 루트 방향을 나타냄

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

class Seat(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)

# Bus 및 user 모델 수정 필요 : 구현 방법 회의 후 결정 필요