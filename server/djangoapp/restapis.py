import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth



def analyze_review_sentiments(url, dealerreview, **kwargs):
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                            auth=HTTPBasicAuth('apikey', "qWYqo3RS6HajH5CEtPeAN2EN44WttMjhDIuK_gFrWcTQ"))
    
    if response.status_code == 200:
        json_data = response.json()
        sentiment_score = json_data['sentiment']['document']['score']
        return sentiment_score
    else:
        print("Error analyzing sentiment:", response.text)
        return None

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', "HHGuPUmQmqb8TldASzYR1FRKzGLB_oqV_pFtRfr_b9ND"))
        print("Network exception occurred2",response)
        
    except:
        print("Network exception occurred")
      
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, nlu_url, **kwargs):
    results = []
    json_result = get_request(url)
    
    if json_result:
        dealers = json_result["dbs"]["rows"]
        
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            
            
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            
            # Perform sentiment analysis on dealer review
            sentiment = analyze_review_sentiments("https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/07c744d3-6940-46c5-a04e-a787b4518fef", dealerreview=dealer_obj, text=dealer_doc["review_text"], version="2021-03-25",
                                                  features="sentiment", return_analyzed_text=True)
            
            if sentiment is not None:
                dealer_obj.sentiment = sentiment
            else:
                dealer_obj.sentiment = 0.0 
            
            results.append(dealer_obj)
    return results

def post_request(url, json_payload, **kwargs):
    requests.post(url, params=kwargs, json=json_payload)