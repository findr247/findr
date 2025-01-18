from .background_runer import get_features, filter_by_text
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ItemImage, Item
from django.core.cache import cache

from .text_filter import search_items


@receiver(post_save, sender=ItemImage)
def add_image_features(sender, instance, created, **kwargs):
    """
    Deletes the image file from storage when a ProductImage instance is deleted.
    """
    filter_model = cache.get('filter_model')
    if created and filter_model:
        get_features(instance, priority=5)


@receiver(post_save, sender=Item)
def item_saved(sender, instance, created, **kwargs):
    filter_by_text(priority=10)

