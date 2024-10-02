from django.db import models


# Create your models here.
from django.db import models

class Watch(models.Model):
    class WatchTypeFunctionality(models.TextChoices):
        QUARTZ = 'Quartz', 'Quartz'
        MECHANICAL = 'Mechanical', 'Mechanical'
        AUTOMATIC = 'Automatic', 'Automatic'
        KINETIC = 'Kinetic', 'Kinetic'
        SMARTWATCH = 'Smartwatch', 'Smartwatch'

    class WatchTypeComplications(models.TextChoices):
        CHRONOGRAPH = 'Chronograph', 'Chronograph'
        DATE_WATCH = 'Date Watch', 'Date Watch'
        GMT = 'GMT', 'GMT'
        MOON_PHASE = 'Moon Phase', 'Moon Phase'
        TOURBILLON = 'Tourbillon', 'Tourbillon'

    company_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=10)
    dial_size = models.IntegerField()  # No max_length for IntegerField
    watch_type_functionality = models.CharField(
        max_length=15,
        choices=WatchTypeFunctionality.choices,
        default=WatchTypeFunctionality.QUARTZ
    )
    watch_type_complications = models.CharField(
        max_length=20,
        choices=WatchTypeComplications.choices,
        default=WatchTypeComplications.CHRONOGRAPH
    )
    description = models.TextField()
    manufacture_date = models.DateField()
    image = models.ImageField(upload_to='watches/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} {self.model_name} ({self.dial_size}mm)"

