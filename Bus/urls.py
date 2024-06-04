from django.urls import path
from .views import home
from . import views

urlpatterns = [
    # 기존 URL 패턴들...
    path('home/', home, name='home'),  # 기존 'home' URL 패턴
    path('route_selection/', views.route_selection, name='route_selection'),
    path('toSuwon/', views.toSuwon, name='toSuwon'),
    path('toSeoul/', views.toSeoul, name='toSeoul'),
    path('board/', views.board, name='board'),
    path('reservation/', views.reservation, name='reservation'),
]