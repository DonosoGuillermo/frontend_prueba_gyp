import pandas as pd
import os

def validar_datos_numericos(data):
    # Verificar si todos los valores son numéricos y mayores a cero en una línea
    if not pd.to_numeric(data['Unidades'], errors='coerce').notnull().all() or (data['Unidades'] <= 0).any():
        return False
    return True

    

def validar_fecha(data):
    try:
        data['Fecha de compra'] = pd.to_datetime(data['Fecha de compra'], format='%d-%m-%Y')
    except ValueError:
        return False
    return True

def validar_unicidad_clase_sku(data):
    # Agrupar los valores de la columna "Clase" por los valores de la columna "SKU" y contar el número de valores únicos en cada grupo
    clase_por_sku = data.groupby('SKU Master')['Clase'].nunique()

    lista = []
    # Seleccionar las filas donde el número de valores únicos es mayor que 1 y mostrar el resultado
    if not (clase_por_sku <= 1).any():
        #El siguiente codigo comentado es para ver los SKU con sus diferentes Clase
        df_resultado = data[data['SKU Master'].isin(clase_por_sku[clase_por_sku > 1].index)]
        df_resultado = df_resultado[['SKU Master', 'Clase']].drop_duplicates()
        lista.append('Los siguientes valores de la columna "SKU" tienen asignados más de un valor de la columna "Clase":')
        #print('Los siguientes valores de la columna "SKU" tienen asignados más de un valor de la columna "Clase":')
        for index, row in df_resultado.iterrows():
            lista.append([row["SKU Master"],row["Clase"]])
        lista_ordenada = sorted(lista, key=lambda x: x[0])
        #for fila in lista_ordenada:
        #    print(f'SKU Master {fila[0]} tiene asignadas las siguientes descripciones: {fila[1]}')
        return lista
    return lista



def corregir_descripcion(data):
    # Agrupar los valores de la columna "Descripción Master" por los valores de la columna "SKU Master" y contar el número de valores únicos en cada grupo
    descripcion_por_sku = data.groupby('SKU Master')['Descripcion Master'].nunique()
    valores_reemplazados = []
    # Seleccionar las filas donde el número de valores únicos es mayor que 1 y corregir las columnas diferentes
    if (descripcion_por_sku > 1).any():
        for sku in descripcion_por_sku[descripcion_por_sku > 1].index:
            valores = data.loc[data['SKU Master'] == sku, 'Descripcion Master']
            valor_mas_comun = valores.value_counts().idxmax()
            data.loc[data['SKU Master'] == sku, 'Descripcion Master'] = valor_mas_comun
            valores_reemplazados.append((sku, valores.unique(), valor_mas_comun))
    '''
    if len(valores_reemplazados) > 0:
        print('Los siguientes valores han sido reemplazados:')
        for sku, valores, valor_nuevo in valores_reemplazados:
            print(f'  SKU: {sku}')
            for valor in valores:
                print(f'    Valor antiguo: {valor}')
            print(f'    Nuevo valor: {valor_nuevo}')
    '''
    return data


def verificar_existencia_columnas(data):
    columnas_requeridas = ['Clase', 'SKU Master', 'Descripcion Master', 'Fecha de compra', 'Unidades', 'Mes', 'Año']
    for columna in columnas_requeridas:
        if columna not in data.columns:
            return False
    return True


def guardar_archivo(data):
    data.to_excel("pacse_gyp_forecast/excel/archivo_reparado.xlsx", index=False)


def eliminar_archivo(nombre):
    ruta = "pacse_gyp_forecast/excel/" + str(nombre)
    if os.path.exists(ruta):
        os.remove(ruta)
