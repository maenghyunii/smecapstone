import os
import django

# Django 프로젝트 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smecapstone.settings')
django.setup()

from Bus.models import Bus  # 'your_app'을 실제 앱 이름으로 변경해야 합니다.

# 버스 데이터를 추가하는 함수
def add_bus_data():
    # 버스 데이터 리스트
    buses = [
        {"name": "인사캠 출발 - 자과캠 도착", "route_direction": "toSuwon"},
        {"name": "자과캠 출발 - 인사캠 도착", "route_direction": "toSeoul"},
    ]
    
    # 리스트를 순회하며 각 버스 데이터에 대한 인스턴스를 생성 및 저장
    for bus in buses:
        bus_instance, created = Bus.objects.get_or_create(
            name=bus["name"],
            defaults={'route_direction': bus["route_direction"]}
        )
        
        if created:
            print(f'버스 "{bus_instance.name}"가 성공적으로 추가되었습니다.')
        else:
            print(f'버스 "{bus_instance.name}"는 이미 존재합니다.')

# 스크립트 실행
if __name__ == "__main__":
    add_bus_data()
