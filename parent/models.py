from django.db import models
from django.contrib.auth.models import User

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Additional fields
    child_username = models.CharField(max_length=100, blank=True, null=True)
    parent_first_name = models.CharField(max_length=100, blank=True, null=True)
    parent_last_name = models.CharField(max_length=100, blank=True, null=True)
    parent_wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'parent_profile'
