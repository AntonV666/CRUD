from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.utils import timezone
from django.db.models import Sum, Avg, Min, Max, Count


def shop(request):
    return render(request, 'catalog/shop.html')


# List of all products
def product_list(request):
    products = Product.objects.all()

    # Фильтрация
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    date_range = request.GET.get('date_range')

    if category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if date_range == '7_days':
        products = products.filter(added_date__gte=timezone.now() - timezone.timedelta(days=7))
    elif date_range == '30_days':
        products = products.filter(added_date__gte=timezone.now() - timezone.timedelta(days=30))

    # Сортировка
    sort_by = request.GET.get('sort_by')
    if sort_by == 'popularity':
        products = products.order_by('-order_count')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'date_asc':
        products = products.order_by('added_date')
    elif sort_by == 'date_desc':
        products = products.order_by('-added_date')

    return render(request, 'catalog/product_list.html', {'products': products})


# Подсчёт общей стоимости всех товаров
total_price = Product.objects.aggregate(Sum('price'))
print(total_price)

# Подсчёт количества товаров в каждой категории
category_counts = Product.objects.values('category').annotate(product_count=Count('id'))
print(category_counts)

# Вывод средней цены товара для каждой категории
avg_price_category = Product.objects.values('category').annotate(avg_price=Avg('price'))
for i in avg_price_category:
    print(f"Category: {i['category']}, Avg Price: {i['avg_price']}")

# Вывод минимальной цены товара для каждой категории
min_price_category = Product.objects.values('category').annotate(min_price=Min('price'))
for i in min_price_category:
    print(f"Category: {i['category']}, Min Price: {i['min_price']}")

# Вывод максимальной цены товара для каждой категории
max_price_category = Product.objects.values('category').annotate(max_price=Max('price'))
for i in max_price_category:
    print(f"Category: {i['category']}, Max Price: {i['max_price']}")


# Creating a new product
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'catalog/create_product.html', {'form': form})


# Reading a single product's details
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


# Updating an existing product
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'catalog/update_product.html', {'form': form})


# Deleting a product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'catalog/delete_product.html', {'product': product})


# Список категорий с общей стоимостью товаров внутри каждой.
def category_total_price(request):
    categories = Product.objects.values('category').annotate(total_price=Sum('price'))
    return render(request, 'catalog/category_total.html', {'categories': categories})


# List of all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'catalog/category_list.html', {'categories': categories})


# Creating a new category
def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'catalog/create_category.html', {'form': form})


# Reading a single category's details
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'catalog/category_detail.html', {'category': category})


# Updating an existing category
def update_category(request, pk):
    category = get_object_or_404(Product, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'catalog/update_category.html', {'form': form})


# Deleting a category
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'catalog/delete_category.html', {'category': category})


# Аналитика с отображением итоговых значений по категориям и общая статистика каталога
def def_analytics(request):
    # Статистика по категориям
    category_stats = Product.objects.values('category').annotate(
        total_price=Sum('price'),
        avg_price=Avg('price'),
        count=Count('id')
    )

    # Общая статистика по каталогу
    shop_stats = Product.objects.aggregate(
        avg_price=Avg('price'),
        total_price=Sum('price'),
        total_items=Count('id'),
        max_price=Max('price'),
        min_price=Min('price')
    )

    return render(request, 'catalog/analytics.html', {
        'category_stats': category_stats,
        'shop_stats': shop_stats,
    })
