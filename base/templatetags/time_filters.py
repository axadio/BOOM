from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def smart_timesince(value):
    if not value:
        return ""

    now = timezone.now()
    # Handle both offset-aware and naive datetimes
    if timezone.is_aware(value):
        diff = now - value
    else:
        diff = timezone.now().replace(tzinfo=None) - value

    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    years = days // 365

    if years >= 1:
        return f"{years} year{'s' if years > 1 else ''}"
    if days >= 1:
        return f"{days} day{'s' if days > 1 else ''}"
    if hours >= 1:
        return f"{hours} hour{'s' if hours > 1 else ''}"
    
    # Defaults to minutes if less than an hour
    return f"{max(0, minutes)} minute{'s' if minutes != 1 else ''}"
