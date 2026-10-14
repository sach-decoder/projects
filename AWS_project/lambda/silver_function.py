import urllib.parse
import awswrangler as wr
import boto3

s3= boto3.client('s3')

def clean_df(df):
    REQUIRED_COLUMNS = {'Store','Date','Weekly_Sales','Holiday_Flag','Temperature','Fuel_Price','CPI','Unemployment'}
    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError(f"Missing columns: {REQUIRED_COLUMNS - set(df.columns)}")

    df_cleaned = df.dropna()
    df_cleaned = df_cleaned.drop_duplicates()
    df_cleaned = df_cleaned.sort_values(by='Date')

    return df_cleaned


def lambda_handler(event, context):
    print("Event received:", event)

    # Extract bucket and file key from event
    record = event['Records'][0]['s3']
    bucket_name = record['bucket']['name']
    source_key = urllib.parse.unquote_plus(record['object']['key'])

    print(f"Source file: s3://{bucket_name}/{source_key}")

    # Read from bronze/
    df = wr.s3.read_csv(path=f"s3://{bucket_name}/{source_key}")

    # Extract original filename
    filename = source_key.split('/')[-1]

    # Target path in silver/
    output_path = f"s3://{bucket_name}/silver/{filename}"
    temp_output_path = f"s3://{bucket_name}/silver/temp_{filename}"
    print(f"Writing output to: {output_path}")
    
    #add cleaned dataframe
    df = clean_df(df)

    try:
        wr.s3.to_csv(df, path=temp_output_path, index=False)

        s3.copy_object(
        Bucket="csvcollection",
        CopySource={"Bucket": "csvcollection", "Key": temp_output_path},
        Key=output_path
        )

        s3.delete_object(Bucket="csvcollection", Key=temp_output_path)
        
    except Exception as e:
        print('There was a error uploading to silver bucket. ')
        raise

    return {"status": "success"}