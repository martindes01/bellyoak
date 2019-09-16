from django import template
from django.template.defaultfilters import stringfilter

import re


register = template.Library()

# RE for final whitespace group in string
re_whitespace = re.compile(r'\s+\S*$')


# Tags

@register.inclusion_tag('bellyoak/tag_recipe_info.html')
def recipe_info(recipe):
    return {
        'recipe': recipe,
    }

@register.inclusion_tag('bellyoak/tag_recipes_list.html')
def recipes_list(recipes):
    return {
        'recipes': recipes,
    }


# Filters

@register.filter()
@stringfilter
def tease(value, args):
    try:
        (min, max) = map(int, args.split(','))

        # Return value with whitespace removed if correct length
        if len(value.strip()) < max:
            return value.strip()

        # Remove leading whitespace and get substring of length (max + 1 - 3)
        # (Extra character may be whitespace indicating end of word)
        # (Three characters removed to accomodate ellipsis)
        value = value.lstrip()[:(max - 3)]

        # Find whitespace group starting at or after (min - 3)
        match = re_whitespace.search(value, min - 3)

        # Return string truncated by word if match found or character if not
        if match:
            # Remove matched whitespace and following characters to leave only full written words
            return value[:match.start()] + '...'
        else:
            # Remove extra character and strip whitespace before appending ellipsis
            return value[:-1].rstrip() + '...'
    except BaseException as error:
        # Return original value with whitespace removed if exception occurs
        print("An exception occurred: {}".format(error))
        return value.strip()
