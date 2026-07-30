# Job Portal

A full-stack job board where employers post listings and job seekers apply — built with Django, with separate authentication and dashboards for each user role.

🔗 **Live demo:** https://jobs.pybrothers.top/
- Recruiter - `username: john` and `password: 1`
- Job Seeker - `username: lucy` and `password: 1`

<img width="1046" height="467" alt="job-3" src="https://github.com/user-attachments/assets/6601b7f3-50d5-467f-b0fa-a5ecd298cfa4" />
<img width="1359" height="634" alt="job-1" src="https://github.com/user-attachments/assets/87d88e39-9d71-41c8-aa11-3d225230132a" />
<img width="1359" height="626" alt="job-2" src="https://github.com/user-attachments/assets/2a6d677a-b46d-4d35-a143-2591311ba716" />


## Features
- Role-based authentication (Employer vs Job Seeker)
- Employers can post, edit, and manage job listings
- Seekers can browse, filter, and apply to jobs
- Application tracking dashboard

## Tech Stack
Python · Django · SQLite/PostgreSQL · HTML/CSS/Bootstrap

## Run Locally
```bash
git clone https://github.com/GRMaruf/Job-Portal.git
cd Job-Portal
pip install -r requirements.txt
python manage.py makemigrations app_base
python manage.py migrate
python manage.py runserver
```

## What I'd Build Next
- Email notifications on new applications
- Admin analytics dashboard
- implement profile cards
