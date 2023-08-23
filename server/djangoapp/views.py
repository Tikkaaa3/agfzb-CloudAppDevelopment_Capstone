from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def post_request(url, data, **kwargs):
    try:
        response = requests.post(url, json=data, **kwargs)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print("Network exception occurred:", e)
        return None


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)
    
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        print("user",user)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/c3c70517-a64e-4389-a494-a4730bd3a2c8/dealership-package/get-dealership.json"
        
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name

        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)  #HttpResponse(dealer_names)
    
    #return render(request, 'index.html', {}) 


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url = f"https://us-south.functions.appdomain.cloud/api/v1/web/c3c70517-a64e-4389-a494-a4730bd3a2c8/dealership-package/get-review.json"
    reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
    
    context['reviews'] = reviews
    context['dealer_id'] = dealer_id
    print("context",context)
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealer_id):
    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        # User is not logged in
        print("User is not logged in")
    else:
        # User is logged in
        print("User `{}` is logged in".format(request.user.username))
        if request.method == 'GET':
        # Handle the GET request logic here
            return render(request, 'djangoapp/add_review.html')
        else:
            review = dict()
            json_payload = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = "John Doe",
            review["dealership"]= "IDK",
            review["review"] = "Great service!",
            review["rating"] = 5,
            review["purchase"]= True
            json_payload["review"] = review
            return post_request("https://us-south.functions.appdomain.cloud/api/v1/web/c3c70517-a64e-4389-a494-a4730bd3a2c8/dealership-package/post-review", json_payload, dealerId=dealer_id)
            


