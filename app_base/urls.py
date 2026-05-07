from django.urls import path
from app_base.views import *

urlpatterns = [
    path('', home, name='home'),
    path('register', User_Register, name='register'),
    path('login', User_Login, name='login'),
    path('logout', User_Logout, name='logout'),

    path('profile/<int:user_id>', profile, name='profile'),
    path('update_profile/<int:user_id>', update_profile, name='update_profile'),

    path('recruiter_dashboard', recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter_dashboard/add_category', add_category, name='add_category'),
    path('recruiter_dashboard/add_skill', add_skill, name='add_skill'),
    path('recruiter_dashboard/update_job/<int:job_id>', update_job, name='update_job'),

    path('find_job', find_job, name='find_job'),
    path('job_details/<int:job_id>', job_details, name='job_details'),
    
    path('apply/<int:job_id>', apply, name='apply'),
    path('seeker_dashboard', seeker_dashboard, name='seeker_dashboard'),
    
    path('show_applicants/<int:job_id>', show_applicants, name='show_applicants'),
]