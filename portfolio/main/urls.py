from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("reviews/submit/", views.submit_review, name="submit_review"),
    path("reviews/<int:review_id>/like/", views.toggle_like, name="toggle_like"),
]
