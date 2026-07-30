# Job Portal

A full-stack job board where employers post listings and job seekers apply — built with Django, with separate authentication and dashboards for each user role.

🔗 **Live demo:** https://jobs.pybrothers.top/
- Recruiter - `username: renold` and `password: demo123`
- Job Seeker - `username: rafi` and `password: rafi123`

<img width="1046" height="467" alt="job-3" src="https://github.com/user-attachments/assets/6601b7f3-50d5-467f-b0fa-a5ecd298cfa4" />

<img width="1339" height="619" alt="job-dashboard" src="https://github.com/user-attachments/assets/0b1ccb16-7ca7-46b1-8c55-831718ed8f40" />

<img width="1357" height="640" alt="job-dashboard 2" src="https://github.com/user-attachments/assets/bd3ef607-f0af-4261-be33-07c039847dd3" />

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
