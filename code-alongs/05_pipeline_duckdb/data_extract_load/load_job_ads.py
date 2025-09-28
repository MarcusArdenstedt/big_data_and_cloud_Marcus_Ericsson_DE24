#========================================#
#                                        #
#    This script loads job ads for       #
#    "Yrken med teknisk inriktning"      #
#                                        #
#========================================#

import dlt
import requests
import json 

dlt.config["load.truncate_staging_dataset"] = True

params = {"limit": 100, "occupation-field": "6Hq3_tKo_V57"}

# API-request, url_for_search is url with endpoint, params is a dictionary with query-parameters that sends with API-request.
def _get_ads(url_for_search, params):
    response = requests.get(url=url_for_search, params= params)
    response.raise_for_status() # check for http errors
    return json.loads(response.content.decode("utf-8"))



# Decoratorn: Ett "lager" ovanpå funktionen som ändrar hur den beter sig eller används.
# Här säger man: "Den här funktionen ska användas som en datakälla i pipeline" 
@dlt.resource(table_name= "technical_field_job_ads", write_disposition= "replace")

def jobads_resource(params):
    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"
    
    
    for ad in _get_ads(url_for_search= url_for_search, params= params):
        yield ad 
        
# dagster only work with source, not resource
# dagster kan bara jobba med en source, inte enskilda resources. 
# Source är ett samlingsobjekt som innehåller en eller flera resources
@dlt.source
def jobads_source():
    return jobads_resource(params)
    

