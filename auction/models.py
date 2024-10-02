from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta


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
    dial_size = models.IntegerField()  
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
    

class Auction(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='open')
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bid_history = models.ManyToManyField('Bid', related_name='auction_bid_history', blank=True)
    bid_increment = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)

    def __str__(self):
        return f"Auction for {self.watch.model_name}"

    def get_bid_history(self):
        return self.bid_history.order_by('-timestamp')

    def extend_auction(self, extra_minutes=5):
        """Extend auction if a bid is placed in the last few minutes."""
        self.end_time += timedelta(minutes=extra_minutes)
        self.save()

    def update_status(self):
        """Update auction status based on end time."""
        if self.end_time < timezone.now():
            self.status = 'closed'
            self.save()

    def notify_winner(self):
        """Send an email notification to the winner when the auction ends."""
        if self.winner:
            send_mail(
                'Congratulations, you won the auction!',
                f'You won the auction for {self.watch.model_name} with a bid of {self.highest_bid}.',
                'auction@example.com',
                [self.winner.email],
                fail_silently=False,
            )

    def get_total_bids(self):
        """Return the total number of bids."""
        return self.bid_history.count()

    def get_average_bid(self):
        """Return the average bid amount."""
        return self.bid_history.aggregate(models.Avg('amount'))['amount__avg']


# Bid model
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return f"Bid by {self.user.username} on {self.auction.watch.model_name}"

