from django.contrib import admin
from .models import Location, Item, ItemImage, UserProfile, ClaimItem, ItemProof

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Location)
admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(ClaimItem)
admin.site.register(ItemProof)


