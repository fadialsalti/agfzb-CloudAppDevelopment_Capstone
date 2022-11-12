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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
