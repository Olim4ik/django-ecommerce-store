from django.urls import path

from store import views

# match with namespace in main urls file
app_name = 'store'


urlpatterns = [
    path('', views.all_products, name='all_produts'),

]
