from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class Product(models.Model):
    """Product Table"""
    unit_in_hours = models.DecimalField(max_digits=10,
                                        decimal_places=2,
                                        default=0.00)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unit_in_hours
