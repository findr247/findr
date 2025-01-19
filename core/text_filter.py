from django.db.models import Q, Count
from .models import Item
import requests

stop_words = set("""a an and are as at be by for from has he in is it its of on that the to was were will with about 
above after again against all am any are because before below between both but by cannot could did do does doing down 
during each few for from further had has have having how if into is it its itself me more most my no nor not now off 
on once only or other over own same should so some such than that the their theirs them themselves then there these 
they this those through too under until very was what when where which while who whom why will with you your yours 
yourself yourselves""".split())

nlp_domain = 'https://findr.pythonanywhere.com/'


def search_items(item):
    query = f'{item.name} {item.description} {item.location}'
    keywords = [word for word in query.split() if word.lower() not in stop_words]
    search_query = Q()

    # Build the query to match keywords
    for word in keywords:
        search_query |= Q(name__icontains=word) | Q(description__icontains=word) | Q(location__name__icontains=word)

    # Annotate each result with a match count and sort by it
    results = (
        Item.objects.filter(search_query)
        .annotate(match_count=Count('id', filter=search_query))
        .order_by('-match_count')  # Sort by the highest match count
    )

    print(results)

    return results


def extract_object_keywords(text):
    response = requests.post(f'{nlp_domain}/keywords', json={
        "sentence": text,
    })

    return response.json()
