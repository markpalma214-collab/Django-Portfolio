from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "maxlength": 1000,
                    "placeholder": "Share your thoughts...",
                    "class": "review-textarea",
                }
            )
        }
        labels = {"message": ""}
