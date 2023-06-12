import pandas as pd
from django.shortcuts import render, get_object_or_404,redirect
from .forms import StatusForm, CategoryForm, StockForm, ProductForm, SalesForm, ForecastForm
from .models import Status, Product, Stock, Category, Sales, Forecast
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.db.models import F
import json



# CRUD Status
def create_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_list')  # Redirige a la vista de obtener todos los registros
    else:
        form = StatusForm()
    
    return render(request, 'create_status.html', {'form': form})

def get_all_status(request):
    statuses = Status.objects.all()
    return render(request, 'status_list.html', {'statuses': statuses})


def get_status_by_id(request, id):
    status = get_object_or_404(Status, id=id)
    return render(request, 'status_detail.html', {'status': status})


def update_status(request, id):
    status = get_object_or_404(Status, id=id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('status_list')
    else:
        form = StatusForm(instance=status)
    
    return render(request, 'update_status.html', {'form': form})

def delete_status(request, id):
    status = get_object_or_404(Status, id=id)
    status.delete()
    return redirect('status_list')

# CRUD Product
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirige a la vista de obtener todos los registros
    else:
        form = ProductForm()
    
    return render(request, 'create_product.html', {'form': form})

def get_all_products(request):
    products = list(Product.objects.all())
    productsJS = serializers.serialize('json', products)
    return HttpResponse(productsJS, content_type='application/json')

def get_product_by_id(request, id):
    try:
        product_data = Product.objects.values('id', 'SKU', 'description', 'restock_time', 'ignored').get(id=id)
        product = Product(**product_data)
        product_json = serializers.serialize('json', [product])
        return JsonResponse(json.loads(product_json)[0]['fields'], safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'update_product.html', {'form': form})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product_list')

## Funciones originadas por CRUD pero necesarias.
def get_info_tabla(request):

    query = Product.objects.values('id', 'SKU', 'description','Category__description', 'Status__name', 'restock_time','ignored')
    query = query.annotate(Category_description=F('Category__description'), Status_name=F('Status__name'))

    data = list(query)

    return JsonResponse(data, safe=False)

# CRUD Stock
def create_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')  # Redirige a la vista de obtener todos los registros
    else:
        form = StockForm()
    
    return render(request, 'create_stock.html', {'form': form})

def get_all_stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})

def get_stock_by_id(request, id):
    stock = get_object_or_404(Stock, id=id)
    return render(request, 'stock_detail.html', {'stock': stock})

def update_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)
    
    return render(request, 'update_stock.html', {'form': form})

def delete_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    stock.delete()
    return redirect('stock_list')

#CRUD Sales
def create_sales(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_list')  # Redirige a la vista de obtener todos los registros
    else:
        form = SalesForm()
    
    return render(request, 'create_sales.html', {'form': form})

def get_all_sales(request):
    sales = Sales.objects.all()
    return render(request, 'sales_list.html', {'sales': sales})


def get_sales_by_id(request, id):
    sales = get_object_or_404(Sales, id=id)
    return render(request, 'sales_detail.html', {'sales': sales})

def get_sales_by_sku(sku):
    try:
        product = Product.objects.get(SKU=sku)
        sales = Sales.objects.filter(Product=product)
        return sales
    except Product.DoesNotExist:
        return None

def update_sales(request, id):
    sales = get_object_or_404(Sales, id=id)
    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sales)
        if form.is_valid():
            form.save()
            return redirect('sales_list')
    else:
        form = SalesForm(instance=sales)
    
    return render(request, 'update_sales.html', {'form': form})

def delete_sales(request, id):
    sales = get_object_or_404(Sales, id=id)
    sales.delete()
    return redirect('sales_list')



#CRUD Forecast
def create_forecast(request):
    if request.method == 'POST':
        form = ForecastForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forecast_list')  # Redirige a la vista de obtener todos los registros
    else:
        form = ForecastForm()
    
    return render(request, 'create_forecast.html', {'form': form})

def get_all_forecasts(request):
    forecasts = Forecast.objects.all()
    return render(request, 'forecast_list.html', {'forecasts': forecasts})

def get_forecast_by_id(request, id):
    forecast = get_object_or_404(Forecast, id=id)
    return render(request, 'forecast_detail.html', {'forecast': forecast})

def get_forecasts_by_sku(sku):
    try:
        product = Product.objects.get(SKU=sku)
        forecasts = Forecast.objects.filter(Product=product)
        return forecasts
    except Product.DoesNotExist:
        return None
    
def get_forecast_and_sales(request, id):
    product = Product.objects.get(id = id)
    forecasts = list(Forecast.objects.filter(Product_id = product.id).order_by('id'))
    sales_product = list(Sales.objects.filter(Product_id = product.id).order_by('id'))

    sales_units_dates = list()
    forecast_units = list()
    forecast_dates = list()

    for sale in sales_product:
        units_dates = list()
        units_dates.append(sale.units)
        units_dates.append(sale.date)
        sales_units_dates.append(units_dates)

    for forecast in forecasts:
        forecast_units.append(forecast.units)
        forecast_dates.append(forecast.date)

    
    df_sales =  pd.DataFrame(sales_units_dates, columns = ['Units', 'Date'])
    df_sales_weekly = df_sales.groupby(pd.Grouper(key='Date',freq='W'))['Units'].sum().reset_index()

    sales_units= df_sales_weekly['Units'].values.tolist()
    sales_dates= df_sales_weekly['Date'].tolist()

    
    data = {'forecast_units': forecast_units,
             'forecast_dates': forecast_dates,
             'sales_units': sales_units,
             'sales_dates': sales_dates}

    return JsonResponse(data, safe = False)
    
    


def update_forecast(request, id):
    forecast = get_object_or_404(Forecast, id=id)
    if request.method == 'POST':
        form = ForecastForm(request.POST, instance=forecast)
        if form.is_valid():
            form.save()
            return redirect('forecast_list')
    else:
        form = ForecastForm(instance=forecast)
    
    return render(request, 'update_forecast.html', {'form': form})

def delete_forecast(request, id):
    forecast = get_object_or_404(Forecast, id=id)
    forecast.delete()
    return redirect('forecast_list')

# CRUD Category
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirige a la vista de obtener todos los registros
    else:
        form = CategoryForm()
    
    return render(request, 'create_category.html', {'form': form})

def get_all_categories(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def get_category_by_id(request, id):
    category = get_object_or_404(Category, id=id)
    return render(request, 'category_detail.html', {'category': category})

def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'update_category.html', {'form': form})

def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('category_list')









