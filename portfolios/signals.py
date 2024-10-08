# portfolios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Portfolio

User = get_user_model()

@receiver(post_save, sender=User)
def create_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)
