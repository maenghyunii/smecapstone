from django.db import models
from user.models import User  

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

#추후에 ~~~~~