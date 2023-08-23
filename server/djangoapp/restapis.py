import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth
from .models import DealerReview



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

# def get_dealer_reviews_from_cf(url, **kwargs):
#     results = []
#     json_result = get_request(url)
#     print("jsonresult",json_result)
#     if json_result:
#         reviews = json_result.get("reviews")  # Access the "reviews" list
        
#         for review_doc in reviews:  # Iterate through the review dictionaries
#               # Use dict.get() for reviews
            
#             if review_doc.get("dealership") == dealer_id:    
#                 dealer_review_obj = DealerReview(
#                         dealership=review_doc.get("dealership", ""),
#                         name=review_doc.get("name", ""),
#                         purchase=review_doc.get("purchase", ""),
#                         review=review_doc.get("review", ""),
#                         purchase_date=review_doc.get("purchase_date", ""),
#                         car_make=review_doc.get("car_make", ""),
#                         car_model=review_doc.get("car_model", ""),
#                         car_year=review_doc.get("car_year", ""),
#                         sentiment=0.0,  # Initialize sentiment, to be updated
#                         id=review_doc.get("id", "")
#                     )
#                 results.append(dealer_review_obj)    
#                 # Perform sentiment analysis on the review
#                 # sentiment = analyze_review_sentiments(
#                 #     "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/07c744d3-6940-46c5-a04e-a787b4518fef",
#                 #     dealerreview=dealer_review_obj,
#                 #     text=review_doc.get("review", ""),
#                 #     version="2021-03-25",
#                 #     features="sentiment",
#                 #     return_analyzed_text=True
#                 # )
                
#                 # if sentiment is not None:
#                 #     dealer_review_obj.sentiment = sentiment
                
#                 # results.append(dealer_review_obj)
    
#     return results

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
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], state=dealer_doc["state"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def post_request(url, json_payload, **kwargs):
    requests.post(url, params=kwargs, json=json_payload)

def get_dealer_by_id(url, dealer_id):
    # Add the dealerId parameter to the URL
    url_with_id = f"{url}?dealerId={dealer_id}"
    # Call get_request with the updated URL
    json_result = get_request(url_with_id)
    if json_result:
        # Create a CarDealer object with the obtained JSON result
        dealer_doc = json_result["doc"]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"])
        return dealer_obj
    return None

def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    json_result = get_request(url)
    
    if json_result:
        reviews = json_result.get("reviews", [])
        
        for review_doc in reviews:
            if review_doc.get("dealership") == dealer_id:
                dealer_review_obj = DealerReview(
                    dealership=review_doc.get("dealership", ""),
                    name=review_doc.get("name", ""),
                    purchase=review_doc.get("purchase", ""),
                    review=review_doc.get("review", ""),
                    purchase_date=review_doc.get("purchase_date", ""),
                    car_make=review_doc.get("car_make", ""),
                    car_model=review_doc.get("car_model", ""),
                    car_year=review_doc.get("car_year", ""),
                    sentiment=0.0,
                    id=review_doc.get("id", "")
                )
                
                results.append(dealer_review_obj)
    
    return results
