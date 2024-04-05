from django.urls import path
from .views import user_login, register, activate 
from . import views # 필요한 뷰들을 임포트

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('mypage/', views.mypage, name='mypage'),
    # 다른 URL 패턴들...
]
