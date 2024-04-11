# delete_users.py
import os
import sys

# 현재 스크립트의 디렉토리 경로를 구합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 디렉토리 경로를 구하기 위해 상위 폴더로 이동
project_root = os.path.dirname(current_dir)
# 프로젝트 루트를 sys.path에 추가
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smecapstone.settings')
import django
django.setup()

from django.contrib.auth.models import User
from user.models import User  # 'your_app'을 실제 앱 이름으로 변경해야 합니다.

def delete_all_users():
    User.objects.all().delete()
    print("모든 사용자 정보가 삭제되었습니다.")

if __name__ == '__main__':
    delete_all_users()
