from pathlib import Path
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from data_extract_load.load_data import tvseries_source
import os


# when running local with dagster, without docker container
# db_path = str(Path(__file__).parents[1]/"data_warehouse/tvseries.duckdb")

# With docker container
DUCKDB_PATH = os.getenv("DUCKDB_PATH")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

#asset
## dlt assets
dlt_resource = DagsterDltResource()

### decorater for assets dlt, create pipeline
@dlt_assets(
    dlt_source= tvseries_source(),
    dlt_pipeline= dlt.pipeline(
        pipeline_name= "tvseries_pipeline",
        destination= dlt.destinations.duckdb(DUCKDB_PATH),  # Removed db_path and replace it with DUCKDB_PATH
        dataset_name= "staging"
    )
)
### instace classes tha needed: dg.AssetExecutionContext is the metadata that dagster need. dlt:DagsterDltResource this is for to run pipeline
def dlt_load(context: dg.AssetExecutionContext, dlt:DagsterDltResource):
    yield from dlt.run(context= context)
    

### dbt assets
#### path to dbt
dbt_project_directory = Path(__file__).parents[1] /"data_transformation"
#### path to profiles for dbt
## Use this when running dagster on local with out docker container
# profiles_dir = Path.home() / ".dbt"

### create a instance for dbt
dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir= DBT_PROFILES_DIR)   # Removed profiles_dir and replace it with DBT_PROFILES_DIR

### Class to run all dbt build, run and test etc. CLI commands for all those
dbt_resource = DbtCliResource(project_dir= dbt_project)

### this type out the manifest, dagster is depended on mainfested and with @dbt_assets it will find it.
dbt_project.prepare_if_dev()

## dbt decorater
### dg.AssetExecutionContext to get metadata from manifest.json
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_model(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context= context).stream()


# jobs
## job_dlt
job_dlt = dg.define_asset_job("job_dlt", selection=dg.AssetSelection.keys("dlt_tvseries_source_df_series"))

## dbt_job
job_dbt = dg.define_asset_job("job_dbt", selection=dg.AssetSelection.key_prefixes("warehouse", "marts"))


# Schedule
schedule_dlt = dg.ScheduleDefinition(
    job= job_dlt,
    cron_schedule= "20 14 * * *"
)

# schedule_dbt = dg.ScheduleDefinition(
#     job= job_dbt,
#     cron_schedule= "22 14 * * *"
# )

# Sensor
@dg.asset_sensor(asset_key= dg.AssetKey("dlt_tvseries_source_df_series"), job_name= "job_dbt")
def dlt_load_sensor():
    yield dg.RunRequest()
    
# definition
defs = dg.Definitions(
    assets= [dlt_load, dbt_model],
    resources= {"dlt": dlt_resource,
                "dbt": dbt_resource},
    jobs= [job_dlt, job_dbt],
    schedules= [schedule_dlt],
    sensors= [dlt_load_sensor]
)