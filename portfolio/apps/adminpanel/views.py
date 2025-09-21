from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.main.models import Project, Skill, Tag
from django.utils.timezone import now
from django.db.models import Count

@login_required
def dashboard(request):
    stats = {
        "projects_count": Project.objects.count(),
        "skills_count": Skill.objects.count(),
        "users_count": User.objects.count(),
    }

    # проекты по тегам
    tags_data = (
        Tag.objects.annotate(projects_count=Count("projects"))
        .values("name", "projects_count")
    )

    # навыки
    skills_data = Skill.objects.values("name", "level")

    # проекты по месяцам (последний год)
    current_year = now().year
    monthly_data = (
        Project.objects.filter(created_at__year=current_year)
        .extra(select={'month': "strftime('%%m', created_at)"})
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    return render(request, "adminpanel/dashboard.html", {
        "stats": stats,
        "tags_data": list(tags_data),
        "skills_data": list(skills_data),
        "monthly_data": list(monthly_data),
    })


@login_required
def projects(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "adminpanel/projects.html", {"projects": projects})


@login_required
def project_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        tags_ids = request.POST.getlist("tags")

        if not title:
            messages.error(request, "Название обязательно!")
        else:
            project = Project.objects.create(
                title=title,
                description=description,
                link=link,
            )
            if tags_ids:
                project.tags.set(tags_ids)
            messages.success(request, "Проект успешно добавлен!")
            return redirect("admin_projects")

    tags = Tag.objects.all()
    return render(request, "adminpanel/project_add.html", {"tags": tags})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.title = request.POST.get("title")
        project.description = request.POST.get("description")
        project.link = request.POST.get("link")
        tags_ids = request.POST.getlist("tags")

        project.save()
        if tags_ids:
            project.tags.set(tags_ids)
        messages.success(request, "Проект обновлён!")
        return redirect("admin_projects")

    tags = Tag.objects.all()
    return render(request, "adminpanel/project_edit.html", {"project": project, "tags": tags})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, "Проект удалён!")
    return redirect("admin_projects")


@login_required
def skills(request):
    skills = Skill.objects.all()
    return render(request, "adminpanel/skills.html", {"skills": skills})


@login_required
def skill_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level")

        Skill.objects.create(name=name, level=level)
        return redirect("admin_skills")

    return render(request, "adminpanel/skill_add.html")


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)

    if request.method == "POST":
        skill.name = request.POST.get("name")
        skill.level = request.POST.get("level")
        skill.save()
        return redirect("admin_skills")

    return render(request, "adminpanel/skill_edit.html", {"skill": skill})


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    return redirect("admin_skills")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("admin_dashboard")  # 👈 сразу в админку
        else:
            messages.error(request, "Неверный логин или пароль")
    
    return render(request, "adminpanel/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("adminpanel-login")
