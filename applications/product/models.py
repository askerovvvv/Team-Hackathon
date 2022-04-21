from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
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
    pub_date = models.DateTimeField(auto_now_add= True)
    # created_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class ProductFavourites(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favouriters')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favouriters')


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    description = models.TextField()
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])  # сам рейтинг оценка от 1 до 5

    def __str__(self):
        return self.description


class Likes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name='like')

    def __str__(self):
        return f'{self.owner}--likes-> {self.product}'
