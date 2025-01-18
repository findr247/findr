from background_task import background
from .models import Item
from django.core.cache import cache

from .text_filter import search_items


@background(schedule=0)
def perform_task(instance_id):
    instance = Item.objects.get(id=instance_id)

    # Perform the task logic (example: log instance details)
    print(f"Performing task for instance: {instance}")


@background(schedule=0)
def get_features(instance):
    filter_model = cache.get('filter_model')
    print(instance.image.url[1:])
    features = filter_model.get_feature(instance.image.url[1:])
    print(features)
    instance.features = features.tolist()
    instance.save()


@background(schedule=0)
def filter_by_text():
    for item in Item.objects.filter(status='lost'):
        results = search_items(item)
        item.relatives.set(results)
        item.save()
        items_not_in_relatives = results.exclude(id__in=item.relatives.values_list('id', flat=True))
