from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Product Serializer objects"""

    class Meta:
        model = Product
        ordering = ['-id']
        fields = ('unit_in_hours', 'user_id')
