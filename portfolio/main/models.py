from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Singleton-ish model holding the hero/about-me content shown on
    Page 1 (Home). Manage this from /admin/ instead of editing HTML.
    """

    name = models.CharField(max_length=100)
    tagline = models.CharField(
        max_length=150,
        blank=True,
        help_text="Short one-line introduction, e.g. 'Full-Stack Developer'.",
    )
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    about = models.TextField(help_text="About-me paragraph shown on the home section.")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class Skill(models.Model):
    name = models.CharField(max_length=80)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional short label/emoji/icon class shown next to the skill.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Hobby(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class PersonalInfo(models.Model):
    """Free-form key/value info shown in the About page grid (e.g. Location: Manila)."""

    label = models.CharField(max_length=80)
    value = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "label"]
        verbose_name_plural = "Personal info"

    def __str__(self):
        return f"{self.label}: {self.value}"


class Project(models.Model):
    title = models.CharField(max_length=120)
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True)
    description = models.TextField(blank=True)
    github_url = models.URLField(help_text="Full GitHub repository URL for this project.")
    technologies = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated list, e.g. 'Django, HTML, CSS, JavaScript'.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]


class SocialLink(models.Model):
    class Platform(models.TextChoices):
        GITHUB = "github", "GitHub"
        LINKEDIN = "linkedin", "LinkedIn"
        FACEBOOK = "facebook", "Facebook"
        INSTAGRAM = "instagram", "Instagram"
        DISCORD = "discord", "Discord"
        REDDIT = "reddit, "Reddit"
        OTHER = "other", "Other"

    platform = models.CharField(max_length=20, choices=Platform.choices)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.get_platform_display()


class Review(models.Model):
    """
    A single testimonial/review from an authenticated user.
    Each user is only allowed to create ONE review (enforced here at the
    DB level with a UniqueConstraint, and again at the view level).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review",
    )
    message = models.TextField(max_length=1000)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_reviews",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user"], name="one_review_per_user")
        ]

    def __str__(self):
        return f"Review by {self.user} ({self.likes.count()} likes)"

    @property
    def like_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter(pk=user.pk).exists()
