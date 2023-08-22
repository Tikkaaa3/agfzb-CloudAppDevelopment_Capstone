import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


def analyze_review_sentiments(url,dealerreview,**kwargs):
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', "HHGuPUmQmqb8TldASzYR1FRKzGLB_oqV_pFtRfr_b9ND"))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', "HHGuPUmQmqb8TldASzYR1FRKzGLB_oqV_pFtRfr_b9ND"))
        print("Network exception occurred2",response)
        
    except:
        # If any error occurs
        print("Network exception occurred")
      
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dbs"]["rows"]
        
        # For each dealer object
        for dealer in dealers:
            
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            print("dealer_doıc",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"],state=dealer_doc["state"])
            print("dealer_doıc9",dealer_obj)
            
            results.append(dealer_obj)
    return results