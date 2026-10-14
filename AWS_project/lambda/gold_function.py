import json
import urllib.parse
import pandas as pd
import awswrangler as wr
import boto3
s3 = boto3.client('s3')

def aggregate_data(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Year'] = df['Date'].dt.year

    holiday_sales = df.groupby('Holiday_Flag')['Weekly_Sales'].sum().reset_index()
    holiday_sales.columns = ['Holiday_Flag', 'Total_Sales']

    total_sales_by_year = df.groupby('Year')['Weekly_Sales'].sum().reset_index()
    total_sales_by_year.columns = ['Year', 'Total_Sales_By_Year']

    avg_unemployment_by_year = df.groupby('Year')['Unemployment'].mean().reset_index()
    avg_unemployment_by_year.columns = ['Year', 'Avg_Unemployment_By_Year']

    avg_cpi_by_year = df.groupby('Year')['CPI'].mean().reset_index()
    avg_cpi_by_year.columns = ['Year', 'Avg_CPI_By_Year']

    total_sales_by_store_year = df.groupby(['Year', 'Store'])['Weekly_Sales'].sum().reset_index()
    total_sales_by_store_year.columns = ['Year', 'Store', 'Total_Sales_By_Store_Year']

    result = total_sales_by_year \
        .merge(avg_unemployment_by_year, on='Year') \
        .merge(avg_cpi_by_year, on='Year') \
        .merge(total_sales_by_store_year, on='Year')

    return result

def lambda_handler(event, context):
    record = event['Records'][0]['s3']
    bucket_name = record['bucket']['name']
    source_key = urllib.parse.unquote_plus(record['object']['key'])

    df = wr.s3.read_csv(path=f"s3://{bucket_name}/{source_key}")
    filename = source_key.split('/')[-1]

    output_path = f"s3://{bucket_name}/gold/{filename}"
    temp_output_path = f"s3://{bucket_name}/gold/temp_{filename}"
    df = aggregate_data(df)
    
    try:
        wr.s3.to_csv(df, path=output_path, index=False)

        s3.copy_object(
        Bucket="csvcollection",
        CopySource={"Bucket": "csvcollection", "Key": output_path},
        Key=temp_output_path
        )

        s3.delete_object(Bucket="csvcollection", Key=temp_output_path)
        
    except Exception as e:
        print('There was a error uploading to silver bucket. ')
        raise
    
    return {"status": "success"}