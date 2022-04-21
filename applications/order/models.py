from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaulttags import now

from applications.product.models import Product

User = get_user_model()


class Status(models.Model):
    status = models.CharField(max_length=50, verbose_name='Название статуса')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    # status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='order_product')
    name = models.CharField(max_length=500)

    def __str__(self):
        return 'Order {}'.format(self.id)

    class Meta:
        # ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_product')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
#     status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='order_product')
#
#     def __str__(self):
#         return '{}'.format(self.id)
#



