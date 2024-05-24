from django.urls import path
from .views import user_login, register, activate, resend_activation_email, injareport, submit_bus_request
from . import views # 필요한 뷰들을 임포트

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('mypage/', views.mypage, name='mypage'),
    path('resend_activation_email/<int:user_id>/', resend_activation_email, name='resend_activation_email'),
    path('logout/', views.user_logout, name='logout'),
    path('manage_no_show/', views.manage_no_show, name='manage_no_show'),
    path('injareport/', injareport, name='injareport'),
    path('submit_bus_request/', submit_bus_request, name='submit_bus_request'),
    path('add_lost_item/', views.add_lost_item, name='add_lost_item'),
    path('add_report/', views.add_report, name='add_report'),
    path('add_post/', views.add_post, name='add_post'),
    path('delete_lost_item/<int:item_id>/', views.delete_lost_item, name='delete_lost_item'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    # 다른 URL 패턴들...
]
