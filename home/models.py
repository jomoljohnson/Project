from django.contrib.auth.models import AbstractUser
from django.db import models

 
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20) # Add any additional fields you need
    email=models.EmailField(unique=True)
    is_mentor = models.BooleanField(default=False)
    admin_id = models.CharField(max_length=10, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    panchayath_name = models.CharField(max_length=100, blank=True, null=True,default='')
    ward_number = models.CharField(max_length=10, blank=True, null=True,default='')
    has_edited_profile = models.BooleanField(default=False)
    def __str__(self):
        self.has_edited_profile = True
        self.save()
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
    job_card_number = models.CharField(max_length=20, blank=True, null=True)
    #user = models.CharField(default='NULL')
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.applicant_name

    def generate_job_card_number(self):
        approved_job_cards = JobCard.objects.filter(approval_status='Approved')
        admin_id = self.user.admin_id if self.user.admin_id else 'XX'
        job_card_count = approved_job_cards.count() + 1
        job_card_number = f'KL-02-003-002-001/{job_card_count:02d}'
        return job_card_number

    def save(self, *args, **kwargs):
        if self.approval_status == 'Approved' and not self.job_card_number:
            self.job_card_number = self.generate_job_card_number()
        super().save(*args, **kwargs)
    


# models.py



class Job(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    remaining_working_days = models.IntegerField(default=100)

class UserSelectedJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, default='Pending') 

class MemberApproval(models.Model):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_selected_job = models.ForeignKey(UserSelectedJob, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Pending')  # 'Pending', 'Approved', 'Rejected'
    rejection_reason = models.TextField(blank=True, null=True)



class Panchayath(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    ward_number = models.CharField(max_length=255)
    member_name = models.CharField(max_length=255)
    member_email = models.EmailField()

    def __str__(self):
        return self.member_name
    
class Complaint(models.Model):
    COMPLAINT_TYPES = [
        ('work_related', 'Work Related'),
        ('job_card_related', 'Job Card Related'),
        ('workers_job_related', "Worker's Job Related"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
    complaint = models.TextField()
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Complaint from {self.user.username}'




class JobAccepted(models.Model):
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    content = models.TextField()
    total_work = models.IntegerField(default=0)
    applied_by = models.CharField(max_length=150)  # Field to store the applied job information
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.worker.username} - {self.job_title}"
    


class UploadedImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    work_date = models.DateField()
    is_present = models.BooleanField(default=False)