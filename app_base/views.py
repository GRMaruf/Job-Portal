from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_base.forms import *
from app_base.models import *

from django.db.models import Q, Count

def home(request):
    return render(request, "home.html")


def User_Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registrations successful.")
            return redirect("login")

    form = RegisterForm()
    context = {"heading": "Registration Form", "form": form}
    return render(request, "auth.html", context)


def User_Login(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login successful.")
            return redirect("home")

    form = LoginForm()
    context = {"heading": "Login Form", "form": form}
    return render(request, "auth.html", context)


@login_required
def User_Logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect("home")


@login_required
def profile(request, user_id):
    user = UserModel.objects.filter(id=user_id).first()
    return render(request, "profile.html", {"user": user})


@login_required
def update_profile(request, user_id):
    user = UserModel.objects.filter(id=user_id).first()
    if user.user_type == "Seeker":
        try:
            profile = user.seeker
        except:
            profile = None
        if request.method == "POST":
            form = SeekerForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, "Profile update successful.")
                return redirect("profile", user_id)

        form = SeekerForm(instance=profile)
    else:
        try:
            profile = user.recruiter
        except:
            profile = None
        if request.method == "POST":
            form = RecruiterForm(request.POST, instance=profile)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, "Profile update successful.")
                return redirect("profile", user_id)

        form = RecruiterForm(instance=profile)

    return render(request, "form.html", {"form": form})


@login_required
def recruiter_dashboard(request):
    jobs = JobPost.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "recruiter_dashboard.html", {"jobs": jobs})


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect("recruiter_dashboard")
        else:
            messages.error(request, f"{ ' '.join(x for x in form.errors['name'])}")
            return redirect("recruiter_dashboard")


@login_required
def add_skill(request):
    if request.method == "POST":
        form = SkillSetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully.")
            return redirect("recruiter_dashboard")
        else:
            messages.error(request, f"{ ' '.join(x for x in form.errors['name'])}")
            return redirect("recruiter_dashboard")


@login_required
def update_job(request, job_id):
    try:
        job = JobPost.objects.get(id=job_id)
    except:
        job = None
    if request.method == "POST":
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            # print(form)
            form = form.save(commit=False)
            form.created_by = request.user
            category = get_object_or_404(Category, id=request.POST.get('category'))
            form.category = category
            form.save()
            form.skill_set.set(request.POST.getlist("skill_set"))
            messages.success(request, "Job posted successfully.")
            return redirect("recruiter_dashboard")
        else:
            messages.error(request, f"{' '.join(x for x in form.errors['name'])}")
            return redirect("update_job")

    form = JobPostForm(instance=job)
    return render(request, "update_job.html", {"form": form})


@login_required
def seeker_dashboard(request):
    try:
        applicant = request.user.seeker
    except:
        messages.warning(request, 'Update your profile first.')
        return redirect('profile', request.user.id)
    
    applications = Applications.objects.filter(applicant=applicant).all()
    waiting_count = applications.aggregate(
        waiting_count = Count('id', filter=Q(status='WAITING'))
    )['waiting_count']
    selected_count = applications.aggregate(
        selected_count = Count('id', filter=Q(status='SELECTED'))
    )['selected_count']
    context = {
        'applications':applications, 
        'waiting_count': waiting_count,
        'selected_count': selected_count
    }
    return render(request, "seeker_dashboard.html", context)

def find_job(request):
    jobs = JobPost.objects.all()
    categories = Category.objects.all()
    
    category = request.GET.get('category')
    search_text = request.GET.get('search_text')
    
    if category:
        jobs = jobs.filter(category=category)
    if search_text:
        jobs = jobs.filter(
            Q(title__icontains = search_text)|
            Q(description__icontains = search_text)|
            Q(skill_set__name__icontains = search_text)
        ).distinct()
    
    jobs = jobs.order_by("-created_at")
    
    context = {
        'jobs':jobs,
        'categories': categories
    }
    return render(request, 'find_job.html', context)

def job_details(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_details.html', {'job': job})

@login_required
def apply(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    try:
        applicant = request.user.seeker
    except:
        messages.warning(request, 'Update your profile first.')
        return redirect('profile', request.user.id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.job = job
            form.applicant = applicant
            form.save()
            messages.success(request, "Job applied successfully.")
            return redirect('seeker_dashboard')
        else:
            messages.error(request, f"{' '.join(x for x in form.errors['name'])}")
    
    form = ApplicationForm()
    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'apply.html', context)

@login_required
def show_applicants(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    applications = Applications.objects.filter(job=job).order_by('-created_at').all()
    
    waiting_count = applications.aggregate(
        waiting_count=Count('id', filter=Q(status='WAITING'))
    )['waiting_count']
    
    selected_count = applications.aggregate(
        selected_count = Count('id', filter=Q(status='SELECTED'))
    )['selected_count']
    
    if request.method == 'POST':
        application_id = request.GET.get('application_id')
        status = request.POST.get('status')
        
        application = get_object_or_404(Applications, id=application_id)
        application.status = status
        application.save()
        
        return redirect('show_applicants', job_id)
    
    
    context = {
        'job': job,
        'applications': applications,
        'waiting_count': waiting_count,
        'selected_count': selected_count,
    }
    return render(request, 'show_applicants.html', context)
    