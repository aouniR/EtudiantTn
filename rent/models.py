from django.db import models

class RentOffer(models.Model):

    ROOM_CHOICES = [
        ('S+0', 'S+0'),
        ('S+1', 'S+1'),
        ('S+2', 'S+2'),
        ('S+3', 'S+3'),
        ('Extra', 'Extra'),
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    rooms = models.CharField(max_length=10, choices=ROOM_CHOICES)
    phone = models.CharField(max_length=8, blank=True)
    price = models.CharField(max_length=4,default=0)
    location = models.TextField()
    pub_date =  models.DateTimeField(auto_now_add=True)

class OfferImage(models.Model):
    offer = models.ForeignKey(RentOffer, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rent_offer_images/')

    def __str__(self):
        return f"Image for {self.offer.title}"
