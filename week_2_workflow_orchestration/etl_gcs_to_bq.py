from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(log_prints=True, retries=3)
def extract_from_gcs(color:str,year:int,month:int, dataset_file:str) ->Path:
    """download data from gcs"""
    gcs_path=f"data\{color}\{dataset_file}.parquet"
    gcs_block= GcsBucket.load("zoom-gcs-2")
    print('found')
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./data/")
    return Path(f"./data/{gcs_path}")

@task()
def transform( path:Path) -> pd.DataFrame:
    """DAta cleaning example"""
    df=pd.read_parquet(path)
    print(f"pre :missing  passenger count:{df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"pre :missing  passenger count:{df['passenger_count'].isna().sum()}")
    return df
@task()
def write_bq(df:pd.DataFrame) -> None:
    """write to big query"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="de-zoomcamp-413508",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="replace",
        )
    
@flow()
def etl_gcs_to_bq():
    """tHE MAIN etll function"""
    color="yellow"
    year=2021
    month=1
    dataset_file=f"{color}_tripsdata_{year}-{month:02}"
    dataset_url="yellow_tripdata_2021-01.csv"
     

    path=extract_from_gcs(color,year,month,dataset_file)
    df=transform(path)
    write_bq(df)
if __name__=="__main__":
    etl_gcs_to_bq()