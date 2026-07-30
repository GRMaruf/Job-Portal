# Job Portal

A full-stack job board where employers post listings and job seekers apply — built with Django, with separate authentication and dashboards for each user role.

🔗 **Live demo:** https://jobs.pybrothers.top/
- Recruiter - `username: john` and `password: 1`
- Job Seeker - `username: lucy` and `password: 1`

![Screenshot](https://drive.google.com/file/d/1zNbtfLW64-e8KduuHT3f1vPz8yK0kmyY/view?usp=sharing)

![Screenshot](https://drive.google.com/file/d/1D9aagbuk577eERO_KEi7C2nM9VR8Rjx0/view?usp=drive_link)

![Screenshot](https://drive.google.com/file/d/1JJOtBn-f_kysg9n9pCHpG6iLbrC3yrHo/view?usp=drive_link)

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
