from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime

class UserManager(BaseUserManager):
    def create_user(self, student_id, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not student_id:
            raise ValueError('Users must have a student ID')

        user = self.model(
            student_id=student_id,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        return self.create_user(student_id, email, password, **extra_fields)

class User(AbstractBaseUser):
    student_id = models.CharField(max_length=10, primary_key=True, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100, blank=False)  # 이름 필드 추가
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    no_show_count = models.IntegerField(default=0)  # 노쇼 횟수
    last_no_show_date = models.DateField(null=True, blank=True)  # 마지막 노쇼 날짜

    objects = UserManager()

    USERNAME_FIELD = 'student_id'  # 이제 학번(사번)이 로그인 식별자가 됩니다.
    REQUIRED_FIELDS = ['email', 'name']  # 회원가입 시 이메일과 이름도 필수로 입력 받습니다.

    def __str__(self):
        return self.email  # 이메일을 반환하거나, 필요에 따라 student_id 또는 name을 반환할 수도 있습니다.

    def has_perm(self, perm, obj=None):
        # 사용자 권한 확인
        return True

    def has_module_perms(self, app_label):
        # 모듈 레벨 권한 확인
        return True

    @property
    def is_staff(self):
        # 관리자 여부 확인
        return self.is_admin

    def record_no_show(self):
        """
        사용자가 노쇼할 경우 호출되는 메서드.
        노쇼 횟수를 증가시키고 마지막 노쇼 날짜를 기록합니다.
        """
        self.no_show_count += 1
        self.last_no_show_date = timezone.now().date()
        self.save()

    def check_suspension_status(self):
        """
        노쇼 이후 일정 기간 동안 이용 정지 여부를 확인하는 메서드.
        """
        if self.last_no_show_date and self.no_show_count > 0:
            suspension_period = datetime.timedelta(days=30)  # 30일간 정지
            return timezone.now().date() - self.last_no_show_date <= suspension_period
        return False