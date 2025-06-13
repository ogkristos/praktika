from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
#Create your models here.
from django.utils.translation import gettext_lazy as _

SELECT_CATEGORY_CHOICES = [
    ("Food", _("Food")),
    ("Travel", _("Travel")),
    ("Shopping", _("Shopping")),
    ("Necessities", _("Necessities")),
    ("Entertainment", _("Entertainment")),
    ("Other", _("Others"))
 ]
ADD_EXPENSE_CHOICES = [
     ("Expense", _("Expense")),
     ("Income", _("Income"))
 ]
PROFESSION_CHOICES =[
    ("Employee", _("Employee")),
    ("Business", _("Business")),
    ("Student", _("Student")),
    ("Other", _("Other"))
]
class Addmoney_info(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    add_money = models.CharField(max_length = 10 , choices = ADD_EXPENSE_CHOICES )
    quantity = models.BigIntegerField()
    Date = models.DateField(default = now)
    Category = models.CharField( max_length = 20, choices = SELECT_CATEGORY_CHOICES , default ='Food')
    class Meta:
        db_table = 'addmoney'
        
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profession = models.CharField(max_length = 10, choices=PROFESSION_CHOICES)
    Savings = models.IntegerField(null=True, blank=True, default=0)  # Добавьте default=0
    income = models.BigIntegerField(null=True, blank=True, default=0)  # Добавьте default=0
    image = models.ImageField(upload_to='profile_image',blank=True)
    def __str__(self):
       return self.user.username

   
# Add these signal handlers
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

