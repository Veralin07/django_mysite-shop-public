from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255)             # CharField
    description = models.TextField()                     # TextField
    price = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField
    quantity = models.PositiveSmallIntegerField()       # PositiveSmallIntegerField
    created_at = models.DateTimeField(auto_now_add=True)  # DateTimeField
    is_active = models.BooleanField(default=True)       # BooleanField
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Order(models.Model):
    notes = models.TextField()                           # TextField
    status = models.CharField(max_length=100)            # CharField
    ordered_at = models.DateTimeField(auto_now_add=True) # DateTimeField
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey к User
    products = models.ManyToManyField(Product)   # ManyToMany с Product
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
