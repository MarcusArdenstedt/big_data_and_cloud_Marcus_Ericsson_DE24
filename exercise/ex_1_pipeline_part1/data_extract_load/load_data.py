import requests
import dlt 


dlt.config["load.truncate_staging_dataset"] = True

# use when don't have dagster
# db_path = str(Path(__file__).parents[1]/"data_warehouse/tvseries.duckdb")

# name for the tv-series 
names = ("game of thrones", "stranger things", "the lord of the ring: the rings of power")

def _get_url(params, endpoint):
    base_url = "https://api.tvmaze.com"
    url_series_id = f"{base_url}/{endpoint}"
    resp = requests.get(url= url_series_id, params= params)
    resp.raise_for_status()
    return resp.json()

def get_serie_id(*names):
    endpoint = "singlesearch/shows"
    name_id = []
    for name in names:
        params = {
            "q": name
        }
        data = _get_url(params= params, endpoint= endpoint)
        name_id.append(data["id"])
    return name_id
    

@dlt.resource(table_name=  "tvserie", write_disposition="replace")
def df_series(*name):
    
    name_id = get_serie_id(*name)
    
    for i in name_id:
        
        url_base = "https://api.tvmaze.com"
        path_params = f"shows/{i}/episodes"
        url_get_serie = f"{url_base}/{path_params}"
        batch = requests.get(url= url_get_serie, timeout=20)
        batch.raise_for_status()
        
        for serie in batch.json():
            yield serie

# dagster works with dlt.source not dlt.resource
@dlt.source
def tvseries_source():
    return df_series(*names)
            
# def run_pipeline(data, table_name):
#     pipeline = dlt.pipeline(
#         pipeline_name = "tvseries_pipeline",
#         destination= dlt.destinations.duckdb(db_path),
#         dataset_name= "staging",
#     )
    
#     load_info = pipeline.run(data,table_name= table_name)
#     print(load_info)
    
# if __name__=="__main__":
#     data = df_series(*names)
#     run_pipeline(data= data, table_name= "got_st_lotr_series")
    
