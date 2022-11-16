from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import *
from .models import CarModel
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

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/get-dealership.json"
        context = {'dealership_list' : get_dealers_from_cf(url)}
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/get-review.json"
        url_dealers = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/get-dealership.json"
        context = {"dealer_reviews" : get_dealer_reviews_from_cf(url, dealer_id), "dealer" : get_dealer_by_id(url_dealers, dealer_id)}
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    url_dealers = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/get-dealership.json"
    context["dealer"] = get_dealer_by_id(url_dealers, dealer_id)
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            if "car" in request.POST.keys():
                car_id = request.POST["car"]
                car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = dealer_id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["id"] = dealer_id + 1
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/eng_fadi77%40hotmail.com_dev/dealership-package/post-review"
            post_request(review_post_url, new_payload, dealer_id=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

