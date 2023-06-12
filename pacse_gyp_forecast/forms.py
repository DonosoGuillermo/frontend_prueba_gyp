from django import forms
from .models import Category, Status, Product, Sales, Forecast,Stock

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'

class ForecastForm(forms.ModelForm):
    class Meta:
        model = Forecast
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

