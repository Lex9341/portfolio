from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("web", "Web"),
        ("ai", "AI"),
        ("game", "Game"),
    ]

    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300, blank=True)  # 🔹 добавлено
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="web")  # 🔹 добавлено
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0, help_text="Уровень в % (0-100)")

    def __str__(self):
        return f"{self.name} ({self.level}%)"


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"
