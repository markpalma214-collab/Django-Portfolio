from django import template
from allauth.socialaccount.models import SocialAccount

register = template.Library()


@register.filter
def google_avatar(user):
    """
    Returns the Google profile picture URL for a user authenticated via
    Google OAuth (django-allauth stores it in SocialAccount.extra_data).
    Falls back to an empty string if unavailable.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return ""
    account = SocialAccount.objects.filter(user=user, provider="google").first()
    if account:
        return account.extra_data.get("picture", "")
    return ""
