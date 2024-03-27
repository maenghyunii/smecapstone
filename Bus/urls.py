# urls.py
from django.urls import path
from .views import home  # 'home' 뷰 함수를 가져옵니다.

urlpatterns = [
    # 기존 URL 패턴들...
    path('home/', home, name='home'),  # 'home' URL 패턴 추가
]