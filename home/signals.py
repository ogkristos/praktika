from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            profession='Other',  # Default value
            Savings=0,          # Default value
            income=0            # Default value
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(
            user=instance,
            profession='Other',  # Default value
            Savings=0,          # Default value
            income=0            # Default value
        )
