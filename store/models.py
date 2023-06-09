from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from core import settings


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # name of the category
    slug = models.SlugField(max_length=255, unique=True)  # url of the category

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self) -> str:
        return self.name
    

class ProductManager(models.Manager):
    # make filtring in model manager -> big models & small and understandable views
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    """ If only we have category, then we can have out Product. If category is deleted all the 
     connected Products also will be deleted """
    category = models.ForeignKey(Category, related_name='product',
                                 on_delete=models.CASCADE)  # connection with category table
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='product_creator')  # connection with user table (User)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # model managers
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self) -> str:
        return self.title
