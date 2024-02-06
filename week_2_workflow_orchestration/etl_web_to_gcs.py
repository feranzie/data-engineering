from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint


@task(log_prints=True, retries=3)
def fetch(dataset_url:str) -> pd.DataFrame:
    """Read dat afrom web to pandas"""
    print('here')
    df=pd.read_csv(dataset_url)
    print('done')
    #if randint(0,1)>0
    return df

@task(log_prints=True)
def clean(df= pd.DataFrame) -> pd.DataFrame:
    "fix dtype issues"
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print(df.head(2))
    print(f"rows: {len(df)}")
    return df
@flow()
def etl_web_gcs() -> None:
    """tHE MAIN etll function"""
    color="yellow"
    print('color')
    year=2021
    month=1
    dataset_file=f"{color}_tripsdata_{year}-{month:02}"
    dataset_url="yellow_tripdata_2021-01.csv"
    print(dataset_file)
    df=fetch(dataset_url)
    df_clean=clean(df)

if __name__ == '__main__':
    etl_web_gcs()




