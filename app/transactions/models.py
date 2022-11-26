from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
STATUS_CHOICES = (
    ("pending", "pending"),
    ("success", "success"),
    ("failed", "failed"),
)

TYPE_CHOICES = (
    ("credit", "credit"),
    ("debit", "debit"),
)


class Transaction(models.Model):
    """Transactions Table"""
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='transaction_product_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='transaction')
    reference = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='pending'
    )
    type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES,
        default='credit'
    )
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 default=0.00)
    payment_channel = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    purchased_hour = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
