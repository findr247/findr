from django.conf import settings

from .models import Item
from django.db.models import Q, Count
import string
from .models import Item
# import spacy
#
# # Load the model
# nlp = spacy.load("en_core_web_sm")

stop_words = set("""a an and are as at be by for from has he in is it its of on that the to was were will with about 
above after again against all am any are because before below between both but by cannot could did do does doing down 
during each few for from further had has have having how if into is it its itself me more most my no nor not now off 
on once only or other over own same should so some such than that the their theirs them themselves then there these 
they this those through too under until very was what when where which while who whom why will with you your yours 
yourself yourselves""".split())


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


# # Example usage
# items = search_items("red wallet")

# # Preprocessing function
# def preprocess_text(text):
#     """Normalize and tokenize text."""
#     stop_words = set(stopwords.words("english"))
#     tokens = word_tokenize(text.lower().translate(str.maketrans('', '', string.punctuation)))
#     return [word for word in tokens if word not in stop_words]
#
#
# # Jaccard Similarity
# def jaccard_similarity(text1, text2):
#     """Calculate Jaccard Similarity between two texts."""
#     set1 = set(preprocess_text(text1))
#     set2 = set(preprocess_text(text2))
#     return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0
#
#
# # Sequence Similarity
# def sequence_similarity(text1, text2):
#     """Calculate Sequence Similarity (Levenshtein ratio)."""
#     return SequenceMatcher(None, text1, text2).ratio()
#
#
# # Combined similarity function
# def calculate_similarity(query_item, db_item):
#     """Calculate combined similarity for name, location, and description."""
#     name_similarity = jaccard_similarity(query_item["name"], db_item.name)
#     location_similarity = sequence_similarity(query_item["location"], db_item.location)
#     description_similarity = jaccard_similarity(query_item["description"], db_item.description)
#     return (0.4 * name_similarity) + (0.3 * location_similarity) + (0.3 * description_similarity)
#
#
# def filter_similar_items(query_item):
#     # Retrieve all items from the database
#     items = Item.objects.all()
#
#     # Calculate similarity for each item
#     results = []
#     for db_item in items:
#         similarity = calculate_similarity(query_item, db_item)
#         if similarity > 0.5:  # Filter items with similarity > 50%
#             results.append({
#                 "item_id": db_item.id,
#                 "name": db_item.name,
#                 "location": db_item.location,
#                 "description": db_item.description,
#                 "similarity": similarity
#             })
#
#     # Sort results by similarity in descending order
#     sorted_results = sorted(results, key=lambda x: x["similarity"], reverse=True)
#
#
# def extract_object_keywords(object_description):
#     description = object_description  # Full descriptive sentence
#
#     # Tokenize and POS tag the description
#     tokens = word_tokenize(description)
#     tagged = pos_tag(tokens)
#
#     # Extract keywords: adjectives (JJ) and nouns (NN, NNP) directly related to the object
#     keywords = []
#     for word, pos in tagged:
#         if pos in {"JJ", "NN", "NNP"} and word.lower() in description.lower():
#             keywords.append(word)
#
#     return keywords
