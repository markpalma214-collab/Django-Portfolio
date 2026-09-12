from django.contrib import admin

from .models import Hobby, PersonalInfo, Profile, Project, Review, SocialLink, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "tagline", "github_url", "linkedin_url")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order")
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "order")
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order")
    search_fields = ("label", "value")
    ordering = ("order", "label")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "github_url", "technologies", "created_at")
    search_fields = ("title", "technologies")
    ordering = ("-created_at",)
    list_filter = ("created_at",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order")
    list_filter = ("platform",)
    ordering = ("order",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "short_message", "like_count", "created_at")
    search_fields = ("user__username", "user__email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def short_message(self, obj):
        return (obj.message[:50] + "...") if len(obj.message) > 50 else obj.message

    def like_count(self, obj):
        return obj.likes.count()
