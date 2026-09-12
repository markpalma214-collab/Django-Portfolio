from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ReviewForm
from .models import Hobby, PersonalInfo, Profile, Project, Review, Skill, SocialLink


def home(request):
    """
    Single-page portfolio: renders all four sections (Home, About,
    Projects, Reviews) in one template so the site scrolls as one
    cohesive page.
    """
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    hobbies = Hobby.objects.all()
    personal_info = PersonalInfo.objects.all()
    projects = Project.objects.all()
    reviews = list(Review.objects.select_related("user").prefetch_related("likes").all())
    for review in reviews:
        review.liked_by_user = review.is_liked_by(request.user)
    socials = SocialLink.objects.all()

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user).first()

    review_form = None
    if request.user.is_authenticated and user_review is None:
        review_form = ReviewForm()

    context = {
        "profile": profile,
        "skills": skills,
        "hobbies": hobbies,
        "personal_info": personal_info,
        "projects": projects,
        "reviews": reviews,
        "socials": socials,
        "user_review": user_review,
        "review_form": review_form,
    }
    return render(request, "main/index.html", context)


@login_required
@require_POST
def submit_review(request):
    """
    Creates the current user's single review. If they already have one,
    this is a no-op redirect (the form is not even shown in that case,
    but we guard here too since this is a security-relevant boundary).
    """
    if Review.objects.filter(user=request.user).exists():
        return redirect("main:home")

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.save()

    return redirect("main:home")


@login_required
@require_POST
def toggle_like(request, review_id):
    """
    AJAX endpoint used by static/main/js/script.js to like/unlike a
    review. Uses Django's normal CSRF-protected session auth — no
    @csrf_exempt anywhere.
    """
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    user = request.user
    if review.likes.filter(pk=user.pk).exists():
        review.likes.remove(user)
        liked = False
    else:
        review.likes.add(user)
        liked = True

    return JsonResponse({"liked": liked, "like_count": review.like_count})
