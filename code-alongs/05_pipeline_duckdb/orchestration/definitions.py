# session imports
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject
from pathlib import Path

# to import dlt script
import sys

sys.path.insert(0, "../data_extract_load")
from load_job_ads_debbie import jobads_source

# data warehouse dircetory
db_path = str(Path(__file__).parents[1] / "data_warehouse/job_ads.duckdb")
# ---------------------------------------------------------------------------

# dlt Assets
## create dlt resource
dlt_resource = DagsterDltResource()


## create dlt asset
@dlt_assets(
    dlt_source=jobads_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobsearch",
        dataset_name="staging",
        destination=dlt.destinations.duckdb(db_path),
    ),
)
def dlt_load(
    context: dg.AssetExecutionContext, dlt: DagsterDltResource
):  # <- if you need loggin data sparas
    ### pydantic, dependency injection, signature: olika namn till dagster
    yield from dlt.run(context=context)


# ---------------------------------------------------------------------------------
# dbt Assets
## related paths for dbt project
dbt_project_directory = Path(__file__).parents[1] / "data_transformation"
profiles_dir = Path.home() / ".dbt"

## create dagster dbt project object
dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir=profiles_dir)

dbt_resource = DbtCliResource(project_dir=dbt_project)

## create a manifest json file
dbt_project.prepare_if_dev()


## create dagster dbt asset
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

#-------------------------------------------------------------

# job
job_dlt = dg.define_asset_job("job_dlt", selection = dg.AssetSelection.keys("dlt_jobads_source_jobads_resource"))


job_dbt = dg.define_asset_job("job_dbt", selection= dg.AssetSelection.key_prefixes("warehouse", "mart"))

# ------------------------------------------------------------------------------------------------------

# Schedule
schedule_dlt = dg.ScheduleDefinition(
    job= job_dlt,
    cron_schedule= "05 13 * * *"
)
# ---------------------------------------------------------

# Sensor
@dg.asset_sensor(asset_key= dg.AssetKey("dlt_jobads_source_jobads_resource"), job_name= "job_dbt")
def dlt_load_sensor():
    yield dg.RunRequest()

# Definitions
defs = dg.Definitions(
    assets=[dlt_load, dbt_models],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    jobs=[job_dlt, job_dbt],
    schedules=[schedule_dlt],
    sensors= [dlt_load_sensor]
)
