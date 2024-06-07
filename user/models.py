from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
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
    name = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    no_show_count = models.IntegerField(default=0)
    last_no_show_date = models.DateField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def record_no_show(self, reason=None):
        """
        사용자가 노쇼할 경우 호출되는 메서드.
        노쇼 횟수를 증가시키고 마지막 노쇼 날짜를 기록합니다.
        """
        self.no_show_count += 1
        self.last_no_show_date = timezone.now().date()
        self.save()

        # NoShow 모델에 기록 추가
        NoShow.objects.create(user=self, date=self.last_no_show_date, reason=reason)

    def check_suspension_status(self):
        """
        노쇼 이후 일정 기간 동안 이용 정지 여부를 확인하는 메서드.
        """
        if self.last_no_show_date and self.no_show_count > 0:
            suspension_period = datetime.timedelta(days=30)
            return timezone.now().date() - self.last_no_show_date <= suspension_period
        return False

class NoShow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.student_id} - {self.date}"

class Report(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title