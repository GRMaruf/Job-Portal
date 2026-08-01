from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.utils import timezone

class UserModel(AbstractUser):
    class UserType(models.TextChoices):
        RECRUITER = 'RECRUITER', 'Recruiter'
        SEEKER = 'SEEKER', 'Seeker'

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.SEEKER
    )

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SkillSet(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RecruiterModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='recruiter')
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(
        upload_to='company/',
        blank=True,
        null=True
    )
    company_address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

    def clean(self):
        if self.user.user_type != UserModel.UserType.RECRUITER:
            raise ValidationError(
                "Only recruiter users can have recruiter profiles."
            )

class SeekerModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='seeker')

    image = models.ImageField(
        upload_to='seeker/',
        blank=True,
        null=True
    )
    objectives = models.TextField(blank=True)

    phone = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    resume = models.FileField(
        upload_to='resume/',
        blank=True,
        null=True
    )

    experience_years = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(
        SkillSet,
        related_name='seekers'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def clean(self):
        if self.user.user_type != UserModel.UserType.SEEKER:
            raise ValidationError(
                "Only seeker users can have seeker profiles."
            )

class JobPost(models.Model):
    created_by = models.ForeignKey(RecruiterModel, on_delete=models.CASCADE, related_name='jobs')

    title = models.CharField(max_length=255)
    openings = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    skill_set = models.ManyToManyField(SkillSet, related_name='jobs')
    required_experience = models.PositiveIntegerField(default=0)
    
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full Time'
        PART_TIME = 'PART_TIME', 'Part Time'
        REMOTE = 'REMOTE', 'Remote'
        INTERNSHIP = 'INTERNSHIP', 'Internship'

    job_type = models.CharField(
        choices=JobType.choices,
        max_length=20
    )

    class JobStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'
        DRAFT = 'DRAFT', 'Draft'

    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.OPEN
    )

    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:80]

    def clean(self):
        if self.salary_min > self.salary_max:
            raise ValidationError(
                "Minimum salary cannot exceed maximum salary."
            )
        if self.deadline < timezone.now().date():
            raise ValidationError(
                "Deadline cannot be in the past."
            )
    
class Application(models.Model):

    class Status(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        REVIEWING = 'REVIEWING', 'Reviewing'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        INTERVIEW = 'INTERVIEW', 'Interview'
        SELECTED = 'SELECTED', 'Selected'
        REJECTED = 'REJECTED', 'Rejected'

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(SeekerModel, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(
        upload_to='resume/',
        blank=True,
        null=True
    )
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.APPLIED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    ) # for recruiter actions.

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'applicant'],
                name='unique_application'
            )
        ]
    def __str__(self):
        name = self.applicant.user.get_full_name() or self.applicant.user.username
        return f'{name} - {self.job.title}'

class SavedJob(models.Model):
    seeker = models.ForeignKey(
        SeekerModel,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['seeker', 'job']

# Activate model validation with:

# obj.full_clean()
# obj.save()

# or override save:

# def save(self, *args, **kwargs):
#     self.full_clean()
#     super().save(*args, **kwargs)