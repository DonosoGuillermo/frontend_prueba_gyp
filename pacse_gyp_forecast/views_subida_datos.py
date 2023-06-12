from django.shortcuts import render
from django.contrib import messages
#from pacse_gyp_forecast.llenado_tablas.subir_info import subir_info_inicial_categoria, subir_info_inicial_status,subir_info_inicial_producto,subir_info_inicial_stock
from pacse_gyp_forecast.llenado_tablas.subir_info import *
from pacse_gyp_forecast.proyecciones.proyecciones import *

from pacse_gyp_forecast.llenado_tablas.verificacion_archivo import *
from pacse_gyp_forecast.llenado_tablas.subir_info import cargar_datos_inicial_bd
from pacse_gyp_forecast.models import Product, Sales, Category,Stock,Status
from django.views.decorators.csrf import csrf_exempt

def subida_inicial_categoria(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo seleccionado no es un archivo Excel válido.')
        else:
            try:
                #AQUI NO HAY VERIFICACIONES
                data = pd.read_excel(excel_file)
                subir_info_inicial_categoria(data)
                messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))
    return render(request, 'subida_categoria.html')

def subida_inicial_status(request):
    if request.method == 'POST':
        try:
            #AQUI NO HAY VERIFICACIONES
            subir_info_inicial_status()
            messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))
    return render(request, 'subida_status.html')


def subida_inicial_producto(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo seleccionado no es un archivo Excel válido.')
        else:
            try:
                #AQUI NO HAY VERIFICACIONES
                data = pd.read_excel(excel_file)
                subir_info_inicial_producto(data)
                messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))
    return render(request, 'subida_categoria.html')


def subida_inicial_stock(request):
    if request.method == 'POST':
        try:
            #AQUI NO HAY VERIFICACIONES
            subir_info_inicial_stock()
            messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))
    return render(request, 'subida_stock.html')

def subida_inicial_venta(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo seleccionado no es un archivo Excel válido.')
        else:
            try:
                data = pd.read_excel(excel_file)
                subir_info_inicial_ventas(data)
                messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))
    return render(request, 'subida_categoria.html')

@csrf_exempt
def subida_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo seleccionado no es un archivo Excel válido.')

        with open("pacse_gyp_forecast/excel/archivo.xlsx", 'wb') as destino:
            for chunk in excel_file.chunks():
                destino.write(chunk)

        data = pd.read_excel("pacse_gyp_forecast/excel/archivo.xlsx", engine='openpyxl')

        if not verificar_existencia_columnas(data):
            messages.error(request, "Revisar el formato del archivo, falta una de las siguientes columnas 'Clase', 'SKU Master', 'Descripcion Master', 'Fecha de compra', 'Unidades', 'Mes', 'Año' ")
            return render(request, 'subida_excel.html')

        data = data[['Clase', 'SKU Master', 'Descripcion Master', 'Fecha de compra','Unidades', 'Mes', 'Año']]
        interruptor = 0

        if not validar_datos_numericos(data):
            messages.error(request, "La columna unidad contiene valores no numericos")
            interruptor = 1
        if not validar_fecha(data):
            messages.error(request, "La columna no esta completamente en formato DD-MM-AA")
            interruptor = 1
            
        resultado_unicidad_clase_sku = validar_unicidad_clase_sku(data)
        if len(resultado_unicidad_clase_sku) != 0: 
            messages.error(request, resultado_unicidad_clase_sku)
            interruptor = 1
        
        if interruptor == 0: 
            cantidad_category = Category.objects.count()
            cantidad_product = Product.objects.count()
            cantidad_status = Status.objects.count()
            cantidad_stock = Category.objects.count()
            cantidad_sales =  Sales.objects.count()

            # Si todas las tablas tienen elementos, se cargan los datos nuevos
            if cantidad_category and cantidad_product and cantidad_status and cantidad_stock and cantidad_sales:
                try:
                    # Se ordena y filtra el dataframe para obtener solo los datos nuevos 
                    dataframe_filtered = sort_cut_dataframe(data)
                    # Se obtienen los SKU de los productos nuevos a proyectar
                    skus_list = dataframe_filtered['SKU Master'].unique()
                    # Se cargan los datos del dataframe en la base de datos
                    cargar_datos_bd(dataframe_filtered)
                    # Se obtiene un nuevo dataframe con todas las ventas de los productos a proyectar
                    sales_dataframe = get_sales_in_bd_dataframe(skus_list)

                    # Aquí aplicamos el forecast, debe haber una función que reciba todos los sku a actualizar
                    forecast_all_products(sales_dataframe,skus_list)



                    print("Carga de datos normal")
                    messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
                except Exception as e:
                    messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))

            else: # Si hay una de estas tablas sin elementos entonces se debe llenar las tablas con la subida inicial
                
                try:
                    # Se ordena y filtra el dataframe para obtener solo los datos nuevos, en este caso al no haber datos, el dataframe debería quedar igual
                    dataframe_filtered = sort_cut_dataframe(data)
                    # Se obtienen los SKU de los productos nuevos a proyectar
                    skus_list = dataframe_filtered['SKU Master'].unique()
                    # Se cargan los datos del dataframe en la base de datos
                    cargar_datos_inicial_bd(dataframe_filtered)
                    sales_dataframe = get_sales_in_bd_dataframe(skus_list)
                    # Aquí aplicamos el forecast, debe haber una función que reciba todos los sku a actualizar
                    # En este caso no deberían obtenerse todas las ventas de la BD, ya que al ser los datos iniciales estarán todas en el dataframe filtrado (dataframe_filtered = data)
                    forecast_all_products(sales_dataframe,skus_list)

                    print("Carga de datos inicial")
                    messages.success(request, 'Los datos se han insertado correctamente en la base de datos.')
                except Exception as e:
                    messages.error(request, 'Ocurrió un error al insertar los datos en la base de datos: ' + str(e))
            
    return render(request, 'subida_excel.html')
