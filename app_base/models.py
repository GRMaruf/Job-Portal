from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    USER_TYPE = [
        ('Recruiter', 'Recruiter'),
        ('Seeker', 'Seeker')
    ]
    user_type = models.CharField(choices=USER_TYPE, max_length=20, default='Seeker')

    def __str__(self):
        return self.username

class RecruiterModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='recruiter')

    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.name[:80]

class SeekerModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='seeker')

    name = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    email = models.EmailField()
    image = models.ImageField(upload_to='seeker/')

    def __str__(self):
        return self.name[:80]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SkillSet(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class JobPost(models.Model):
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='jobs')

    title = models.CharField(max_length=255)
    openings = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='Undefined')
    description = models.TextField(blank=True)
    skill_set = models.ManyToManyField(SkillSet, related_name='skill_set')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:80]
    
class Applications(models.Model):

    STATUS = {
        ('APPLIED', 'APPLIED'),
        ('WAITING', 'WAITING'),
        ('SELECTED', 'SELECTED'),
    }
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(SeekerModel, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resume/')
    status = models.CharField(choices=STATUS, max_length=20, default='APPLIED')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant.name} - {self.job.title}'