from django.db import models
from django.utils.timezone import now
from django.core.validators import MinLengthValidator

class CarMake(models.Model):
    name = models.CharField(max_length=30, help_text='Enter a make (e.g. Dodge)', 
    validators=[MinLengthValidator(2, "Make must be greater than 1 character")])
    description = models.TextField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class CarModel(models.Model):
    choices = [('Sedan','Sedan'), ('SUV','SUV'), ('Wagon','Wagon'), ('Sport','Sport')]
    name = models.CharField(max_length=30,
            validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")])
    dealer_id = models.PositiveIntegerField()
    type = models.CharField(
        max_length=10,
        choices=choices,
        default='Sedan',
    )
    year = models.DateField()
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, null=False)
    def __str__(self):
        """String for representing the Car Model object."""
        return self.name

# Create a plain Python class `CarDealer` to hold dealer data
class CarDealer():
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# Create a plain Python class `DealerReview` to hold review data
class DealerReview():
    def __init__(self, dealership, name, id, review, purchase_date=None, car_make=None, car_model=None, car_year=None, purchase=False, sentiment='netural'):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id 

    def __str__(self):
        return "Reviewer name: " + self.name + " - review: " + self.review