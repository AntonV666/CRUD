from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product/', views.product_list, name='product_list'),
    path('product/new/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('category/', views.category_list, name='category_list'),
    path('category/total/', views.category_total_price, name='category_total'),
    path('category/new/', views.create_category, name='create_category'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('category/<int:pk>/edit/', views.update_category, name='update_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('analytics/', views.def_analytics, name='analytics'),
]