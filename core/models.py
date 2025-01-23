from django.db import models
from django.contrib.auth.models import User
import numpy as np


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    matric_no = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('returned', 'Returned'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    location = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    date = models.DateTimeField(auto_now=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_items")
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="claimed_items")
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    relatives = models.ManyToManyField('self', blank=True)
    questions = models.JSONField(default=list, blank=True)
    answers = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to="item_images/", blank=True, null=True)
    features = models.JSONField(null=True, blank=True)

    def features_data(self):
        return np.array(self.features)


class ClaimItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claim')
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_claimed')
    claimed_on = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=50)
    answers = models.JSONField(default=list, blank=True)


class ItemProof(models.Model):
    claim = models.ForeignKey(ClaimItem, on_delete=models.CASCADE, related_name='image_proof')
    image = models.ImageField(upload_to='proof_images/')

