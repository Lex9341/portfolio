from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .models import Project, Skill, Tag, Achievement
from .forms import ContactForm


def home(request):
    projects = Project.objects.all().order_by("-created_at")
    skills = Skill.objects.order_by("-level")
    tags = Tag.objects.all()
    achievements = Achievement.objects.order_by("-date")[:5]

    return render(request, "main/home.html", {
        "projects": projects,
        "skills": skills,
        "tags": tags,
        "achievements": achievements,
    })


def projects(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, "main/projects.html", {"projects": projects})


def skills(request):
    skills = Skill.objects.all().order_by("-level")
    return render(request, "main/skills.html", {"skills": skills})


def about(request):
    return render(request, "main/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()

            # отправляем email
            send_mail(
                subject=f"Новое сообщение с портфолио от {message.name}",
                message=f"Имя: {message.name}\nEmail: {message.email}\n\nСообщение:\n{message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(request, "✅ Спасибо! Ваше сообщение отправлено.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})
