from django import template

register = template.Library()


@register.filter
def get_item(lst, index):
    try:
        return lst[int(index)]  # Convert index to integer
    except (IndexError, ValueError, TypeError):
        return None  # Handle out-of-range or invalid cases
