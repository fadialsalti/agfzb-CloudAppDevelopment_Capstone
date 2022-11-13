from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/get-review.json"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        print(dealer_reviews)
        reviews = ' '.join([review.review for review in dealer_reviews])
        sentiments = ' '.join([review.sentiment for review in dealer_reviews])
        return HttpResponse(reviews+'<br>'+sentiments)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        username = request.user.username
        print(request.POST)
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/post-review"
        review = {}
        # example data to be repalced by form from user
        # TODO: prevent double post requests or duplicate data
        review["dealership"] = dealer_id
        review["name"] = "Saleh Sawaad"
        review["purchase"] = True
        review["review"] = "This is a great car dealer"
        review["purchase_date"] = datetime.utcnow().isoformat()
        review["car_make"] = "Audi"
        review["car_model"] = "A6"
        review["car_year"] = 2005
        review["id"] = 9
        json_payload = {"review": review}
        resp=post_request(url, json_payload)
        return HttpResponse(json.dumps(resp), content_type="application/json")


