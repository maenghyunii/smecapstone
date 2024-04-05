from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Bus(models.Model):
    name = models.CharField(max_length=100)
    route_direction = models.CharField(max_length=50)  # toSuwon or toSeoul

    def __str__(self):
        return f"{self.name} ({self.route_direction})"

class Schedule(models.Model):
    bus = models.ForeignKey(Bus, related_name='schedules', on_delete=models.CASCADE)
    departure_time = models.TimeField()
    departure_date = models.DateField()  # 스케줄 날짜 추가

    def __str__(self):
        return f"{self.bus.name} - {self.departure_date} {self.departure_time}"

class Seat(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_reserved = models.BooleanField(default=False)  # 좌석 예약 여부 확인

    def __str__(self):
        status = "Reserved" if self.is_reserved else "Available"
        return f"{self.schedule} - Seat {self.seat_number} ({status})"

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reservations', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='reservations', on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.seat}"


# Bus 및 user 모델 수정 필요 : 구현 방법 회의 후 결정 필요