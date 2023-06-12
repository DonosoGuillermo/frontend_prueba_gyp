import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from pmdarima.arima import auto_arima, ndiffs, nsdiffs
from pacse_gyp_forecast.models import Product, Forecast, Sales

def get_sales_in_bd_dataframe(skus_list):

    data = []

    for sku in skus_list:
        try:
            product_bd = Product.objects.get(SKU = sku)
            sales_by_product = Sales.objects.filter(Product_id = product_bd.id)

            for sale in sales_by_product:
                data.append({
                    'SKU': sku,
                    'Date': sale.date,
                    'Units': sale.units
                })
        
        except Product.DoesNotExist:
            # Manejar el caso en el que el SKU no exista en la base de datos
            print(f"El SKU '{sku}' no existe")
    
    # Crear el dataframe a partir de la lista de diccionarios
    df = pd.DataFrame(data)
    return df
        
def list_all_SKUs(sales_df):
    
    all_SKUs = sales_df['SKU'].unique()

    return all_SKUs


def filter_SKU(sales_df, SKU_product):
    
    sales_df_product = sales_df[sales_df['SKU'] == SKU_product]
    sales_df_product = sales_df_product.groupby(pd.Grouper(key='Date',freq='W'))['Units'].sum()
    sales_df_product = sales_df_product.reset_index()
    
    return sales_df_product


def evaluate_diff(sales_ts, periods):

    d_value = ndiffs(x = sales_ts,
                     alpha = 0.05,
                     test = 'adf')
    
    D_value = nsdiffs(x = sales_ts,
                      m = periods,
                      test = 'ch')
    
    return D_value , d_value
    
def generate_predictions(sales_ts, D_value, d_value, periods):

    sarima_model = auto_arima(sales_ts,
                              test = 'adf',
                              d = d_value,
                              seasonal = True,
                              seasonal_test = 'ch',
                              D = D_value,
                              m = periods,
                              trace = False,
                              max_order = None)

    predictions = sarima_model.predict(n_periods = 24)

    return predictions

def generate_future_date(df_date_product, n_dates):
    
    recent_date = df_date_product.max()

    list_future_date = []

    i = 1
    while i <= n_dates:
        new_date = recent_date + timedelta(weeks = i)
        list_future_date.append(new_date.date())
        i = i + 1
    return list_future_date


def forecast_all_products(sales_df, list_SKUs):
    
    for SKU in list_SKUs:
        sales_df_product = filter_SKU(sales_df, SKU)
        sales_ts_product = sales_df_product['Units'].values.tolist()
        Diff_value, diff_value = evaluate_diff(sales_ts_product, 52)


        predictions = generate_predictions(sales_ts_product, Diff_value, diff_value, 52)
        future_date = generate_future_date(sales_df_product['Date'], 24)


        product_to_update = Product.objects.get(SKU = SKU)
        list_forecast = Forecast.objects.filter(Product_id = product_to_update.id).order_by('id')
        if list_forecast:
            
            i = 0
            for forecast in list_forecast:
                forecast.objects.update(date = future_date[i],
                                        units = round(predictions[i]))
                i = i + 1
        else:
            
            i = 0
            while i < 24:
                forecast = Forecast.objects.create(date = future_date[i],
                                                   units = round(predictions[i]),
                                                   Product_id = product_to_update.id)
                forecast.save()
                i+=1

    return True
