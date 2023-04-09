from django.urls import path

from store import views

# match with namespace in main urls file
app_name = 'store'


urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('shop/<slug:caregory_slug>', views.category_list, name="category_list"),
]
