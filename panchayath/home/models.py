from django.contrib.auth.models import AbstractUser
from django.db import models

 
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20) # Add any additional fields you need
    email=models.EmailField(unique=True)
    is_mentor = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    


class JobCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    applicant_name = models.CharField(max_length=100)  # Add this foreign key field
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    house_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    panchayath = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    ration_card_number = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    household_latrine = models.BooleanField()
    indira_avas_yojana = models.BooleanField()
    rofr_act = models.BooleanField()
    APPROVAL_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='Pending')
    #user = models.CharField(default='NULL')
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.applicant_name
    


