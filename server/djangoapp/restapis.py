import requests
import json, os
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
# import and load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('api_key')

# Create a `get_request` to make HTTP GET requests
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)
    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        try:
            reviews = json_result['body']['data']['docs']
            for dealer_doc in reviews:
                review_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"], purchase=dealer_doc["purchase"],
                                    review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"], car_make=dealer_doc["car_make"],
                                    car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"], id=dealer_doc["id"], 
                                    sentiment=analyze_review_sentiments(dealer_doc["review"]))
                print(review_obj)
                results.append(review_obj)
        except KeyError:
            print("Dealership doesn't exist")
    return results

def get_dealer_by_id(url, dealerId):
    json_result = get_request(url, id=dealerId)
    if json_result:
        dealer_doc = json_result['result']
        dealer = next(dealer for dealer in dealer_doc if dealer['id'] == dealerId)
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                            id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                            short_name=dealer["short_name"],
                            st=dealer["st"], zip=dealer["zip"])
    return dealer_obj

def get_dealer_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        dealer = json_result["result"]
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                            id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                            short_name=dealer["short_name"],
                            st=dealer["st"], zip=dealer["zip"])
        results.append(dealer_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/4db1c8c8-6c6d-415f-a81d-d4d6fcab07c0" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze(text=text, features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    return label


