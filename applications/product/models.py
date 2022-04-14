from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(max_length=30, primary_key=True)

    def __str__(self):
        return self.slug


class Product(models.Model):
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


