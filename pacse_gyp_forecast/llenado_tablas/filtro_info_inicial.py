import pandas as pd

# DETALLE ARCHIVO
# En este archivo se definen funciones que tienen la finalidad de filtrar la información inicial 
# para rellenar las tablas de la BD


# Objetivo: Esta columna entra las filas de una columna sin repetición, se puede usar para llenar la tabla Category

# Entradas
#   variable file_path: String que puede corresponder a la ruta en que se encuentra un archivo, o el nombre del archivo si este se encuentra en la misma
#                        carpeta que este código
#   variable sheet_name: String que contiene el nombre de la sheet a utilizar del archivo excel, el estandar a utilizar
#                        es "Detalle Consolidado"
#   variable column_name: String con el nombre de la columna de la cual se quieren obtener los valores únicos

# Salidas:
#   variable unique_values: Arreglo con los valores únicos de la columna específicada en la entrada

def obtener_info_columna_específica(dataframe, column_name):
    # Leer el archivo Excel en un dataframe de pandas
    #df = pd.read_excel(file_path, sheet_name=sheet_name)
    df = dataframe.copy()

    # Filtrar la columna específica
    column = df[column_name]
    
    # Obtener los elementos únicos de la columna
    unique_values = column.unique()
    
    # Retornar los elementos únicos de la columna
    return unique_values


nombre_excel = 'Ventas Ene2021 @Mar2023 ER.xlsx'
nombre_sheet = 'Detalle Consolidado'
nombre_columna_unica = 'Descripcion Master'
columnas_seleccionadas = ['Clase', 'SKU Master', 'Descripcion Master']
columna_filtro_unico = 'SKU Master'

#unique_values = obtener_info_columna_específica( nombre_excel, nombre_sheet, nombre_columna)
#archivo_salida = 'salida.xlsx'
#df.to_excel(archivo_salida, index=False)
#___________________________________________________________________________________________________________________________________________________



# Objetivo: Funcion que entrega toda la información que se puede obtener desde el excel para rellenar la tabla de productos

# Entradas
#   variable file_path: String que puede corresponder a la ruta en que se encuentra un archivo, o el nombre del archivo si este se encuentra en la misma
#                        carpeta que este código
#   variable sheet_name: String que contiene el nombre de la sheet a utilizar del archivo excel, el estandar a utilizar
#                        es "Detalle Consolidado" 

# Salidas:
#   variable df: Es un dataframe de pandas que contiene solo las columnas ['Clase', 'SKU Master', 'Descripcion Master'],
#                este contiene los productos por SKU sin repetición y con la columna Clase con la respectiva llave foránea.

def obtener_info_productos(dataframe):
    nombre_columna_clase = 'Clase'
    columnas_seleccionadas = ['Clase', 'SKU Master', 'Descripcion Master']
    columna_filtro_unico = 'SKU Master'

    # Lee el archivo Excel en un dataframe
    #df = pd.read_excel(file_path, sheet_name=sheet_name)
    df = dataframe.copy()

    # Obtiene todas las categorías únicas
    categorias = df[nombre_columna_clase].unique()

    # Se selecciona solo las columnas usadas en producto
    df = df[columnas_seleccionadas]
    
    # Elimina las filas duplicadas basadas en la columna SKU Master
    df = df.drop_duplicates(subset=[columna_filtro_unico])
        
    # Itera sobre cada fila y cambia el valor de la columna Clase por su índice en la variable categorias
    for index, row in df.iterrows():
        categoria = row[nombre_columna_clase]
        indice = categorias.tolist().index(categoria)
        df.at[index, nombre_columna_clase] = indice+1
    
    return df

#obtener_info_productos(nombre_excel,nombre_sheet)


##########################################################################################################################

# Objetivo: Esta columna entra las filas de una columna sin repetición, se puede usar para llenar la tabla Category

# Entradas
#   variable df: Corresponde al dataframe al cual se le harán las modificaciones
#   variable column_name: String con el nombre de la columna de la cual se quieren obtener los valores únicos

# Salidas:
#   variable unique_values: Arreglo con los valores únicos de la columna específicada en la entrada

def obtener_info_columna_específica_df(dataframe, column_name):
    df = dataframe.copy()
    # Filtrar la columna específica
    column = df[column_name]
    
    # Obtener los elementos únicos de la columna
    unique_values = column.unique()
    
    # Retornar los elementos únicos de la columna
    return unique_values

#___________________________________________________________________________________________________________________________________________________

# Objetivo: Funcion que entrega un dataframe toda la información que se puede obtener desde el excel para rellenar la tabla de productos

# Entradas
#   variable df: Es el dataframe inicial del cual se obtendrá la información para rellenar la tabla productos.
#   variable categorias: Arreglo con las categorias guardadas en la base de datos

# Salidas:
#   variable df: Es un dataframe de pandas que contiene solo las columnas ['Clase', 'SKU Master', 'Descripcion Master'],
#                este contiene los productos por SKU sin repetición y con la columna Clase con la respectiva llave foránea.

def obtener_info_inicial_productos_df(dataframe,categorias):
    nombre_columna_clase = 'Clase'
    columnas_seleccionadas = ['Clase', 'SKU Master', 'Descripcion Master']
    columna_filtro_unico = 'SKU Master'

    df = dataframe.copy()
    # Obtiene todas las categorías únicas
    #categorias = df[nombre_columna_clase].unique()

    # Se selecciona solo las columnas usadas en producto
    df = df[columnas_seleccionadas]
    
    # Elimina las filas duplicadas basadas en la columna SKU Master
    df = df.drop_duplicates(subset=[columna_filtro_unico])
    
    # Itera sobre cada fila y cambia el valor de la columna Clase por su índice en la variable categorias
    for index, row in df.iterrows():
        categoria = row[nombre_columna_clase]
        indice = categorias.index(categoria)
        df.at[index, nombre_columna_clase] = indice+1
    
    return df

#___________________________________________________________________________________________________________________________________________________

# Objetivo: Funcion que entrega un dataframe toda la información que se puede obtener desde el excel para rellenar la tabla de sales

# Entradas
#   variable df: Es el dataframe inicial del cual se obtendrá la información para rellenar la tabla sales.
#   variable productos: Arreglo con los sku de los productos guardados en la base de datos

# Salidas:
#   variable df: Es un dataframe de pandas que contiene solo las columnas ['Clase', 'SKU Master', 'Descripcion Master'],
#                este contiene los productos por SKU sin repetición y con la columna Clase con la respectiva llave foránea.

#en este caso categorias ahora es prodcutos
#
def obtener_info_inicial_sales_df(dataframe,productos):
    nombre_columna_SKU = 'SKU Master'
    columnas_seleccionadas = ['SKU Master', 'Fecha de compra', 'Unidades']
    
    df = dataframe.copy()
    # Se selecciona solo las columnas usadas en producto
    df = df[columnas_seleccionadas]
    
    # Itera sobre cada fila y cambia el valor de la columna Clase por su índice en la variable categorias
    for index, row in df.iterrows():
        producto = row[nombre_columna_SKU]
        indice = productos.index(producto)
        df.at[index, nombre_columna_SKU] = indice+1
    
    return df