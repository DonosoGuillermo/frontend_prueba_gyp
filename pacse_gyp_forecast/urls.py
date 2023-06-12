

from django.urls import path
from pacse_gyp_forecast.views_subida_datos import subida_inicial_categoria,subida_inicial_status,subida_inicial_producto,subida_inicial_stock
from pacse_gyp_forecast.views_subida_datos import subida_inicial_venta
from pacse_gyp_forecast.views_subida_datos import subida_excel
from pacse_gyp_forecast.views_crud import get_info_tabla, get_forecast_and_sales, get_product_by_id


app_name = 'pacse_gyp_forecast'

urlpatterns = [
    path('subida_categoria/', subida_inicial_categoria, name = 'subida_categoria'),
    path('subida_status/', subida_inicial_status, name = 'subida_status'),
    path('subida_producto/', subida_inicial_producto, name = 'subida_producto'),
    path('subida_stock/', subida_inicial_stock, name = 'subida_stock'),
    path('subida_venta/', subida_inicial_venta, name = 'subida_venta'),
    path('subida_excel/', subida_excel, name = 'subida_excel'),
    path('productos/', get_info_tabla, name = 'get_info_tabla'),
    path('productos/<int:id>', get_product_by_id, name='get_product_by_id'),
    path('predicciones/<int:id>', get_forecast_and_sales, name='get_forecast_and_sales')
]
