from django.urls import path

from store_basket import views

app_name = 'store_basket'

urlpatterns = [
    path('', views.basket_summary, name="basket_summary"),
    path('add/', views.basket_add, name="basket_add")
]
