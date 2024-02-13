from pathlib import Path
import pandas as pd
from prefect import flow, task
#from prefect_gcp.cloud_storage import GcsBucket
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

@task()
def write_local(df: pd.DataFrame,color:str,dataset_file:str)-> Path:
    """write dataframe out locally a parquet"""
    path=Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path,compression="gzip")
    return path

@task()
def write_gcs(path:Path)-> None:
    """write to gcs"""
    print("gooogle buckettt")
    gcs_block=GcsBucket.load("zoom-gcs-2")
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path)
    return
    

@flow()
def etl_web_gcs() -> None:
    """tHE MAIN etll function"""
    color="yellow"
    year=2021
    month=1
    dataset_file=f"{color}_tripsdata_{year}-{month:02}"
    dataset_url=""
    print(dataset_file)
    df=fetch(dataset_url)
    df_clean=clean(df)
    path=write_local(df_clean,color,dataset_file)
    write_gcs(path)

if __name__ == '__main__':
    etl_web_gcs()




