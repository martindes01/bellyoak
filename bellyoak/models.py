from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from decimal import Decimal

# TODO
# Research integer and decimal validation
# Add length, more units, imperial
# Add course, cuisine, publish/update dates, tags
# Choose upload_to locations and filenames
# Overwrite uploaded files

class Recipe(models.Model):
    class Diet():
        NONE = 'none'
        VEGETARIAN = 'vegetarian'
        VEGAN = 'vegan'

        DIET_CHOICES = [
            (NONE, 'None'),
            (VEGETARIAN, 'Vegetarian'),
            (VEGAN, 'Vegan'),
        ]

    # author = models.ManyToManyField(User)
    title = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='recipe_images', blank=True)
    description = models.TextField(blank=True)
    # preparation_time = models.DurationField(blank=True, null=True)
    # cooking_time = models.DurationField(blank=True, null=True)
    servings = models.IntegerField(default=1)
    diet = models.CharField(max_length=255, choices=Diet.DIET_CHOICES, default=Diet.NONE)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=63)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.servings < 1:
            self.servings = 1

        if self.likes < 0:
            self.likes = 0

        if self.views < 0:
            self.views = 0

        self.slug = slugify(self.title[:63])

        super().save(*args, **kwargs)

class Ingredient(models.Model):
    class Unit():
        SYMBOL_KEY = 'symbol'
        NAME_KEY = 'name'

        NONE = 'none'
        GRAM = 'gram'
        KILOGRAM = 'kilogram'
        MILLILITRE = 'millilitre'
        LITRE = 'litre'
        TEASPOON = 'teaspoon'
        TABLESPOON = 'tablespoon'
        CUP = 'cup'
        PINT = 'pint'

        units = {
            GRAM: {
                SYMBOL_KEY: 'g',
                NAME_KEY: 'grams',
            },
            KILOGRAM: {
                SYMBOL_KEY: 'kg',
                NAME_KEY: 'kilograms',
            },
            MILLILITRE: {
                SYMBOL_KEY: 'ml',
                NAME_KEY: 'millilitres',
            },
            LITRE: {
                SYMBOL_KEY: 'l',
                NAME_KEY: 'litres',
            },
            TEASPOON: {
                SYMBOL_KEY: 'tsp',
                NAME_KEY: 'teaspoons',
            },
            TABLESPOON: {
                SYMBOL_KEY: 'tbsp',
                NAME_KEY: 'tablespoons',
            },
            CUP: {
                SYMBOL_KEY: 'cup',
                NAME_KEY: 'cups',
            },
            PINT: {
                SYMBOL_KEY: 'pt.',
                NAME_KEY: 'pints',
            },
        }

        UNIT_CHOICES = [
            (NONE, 'None'),
            ('Mass', (
                    (GRAM, units[GRAM][SYMBOL_KEY] + ' (' + units[GRAM][NAME_KEY] + ')'),
                    (KILOGRAM, units[KILOGRAM][SYMBOL_KEY] + ' (' + units[KILOGRAM][NAME_KEY] + ')'),
                )
            ),
            ('Volume', (
                    (MILLILITRE, units[MILLILITRE][SYMBOL_KEY] + ' (' + units[MILLILITRE][NAME_KEY] + ')'),
                    (LITRE, units[LITRE][SYMBOL_KEY] + ' (' + units[LITRE][NAME_KEY] + ')'),
                    (TEASPOON, units[TEASPOON][SYMBOL_KEY] + ' (' + units[TEASPOON][NAME_KEY] + ')'),
                    (TABLESPOON, units[TABLESPOON][SYMBOL_KEY] + ' (' + units[TABLESPOON][NAME_KEY] + ')'),
                    (CUP, units[CUP][SYMBOL_KEY] + ' (' + units[CUP][NAME_KEY] + ')'),
                    (PINT, units[PINT][SYMBOL_KEY] + ' (' + units[PINT][NAME_KEY] + ')'),
                )
            ),
        ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', related_query_name='ingredient')
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal())
    unit = models.CharField(max_length=255, choices=Unit.UNIT_CHOICES, default=Unit.NONE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure quantity positive with max digits 9 and decimal places 2
        parts = str(self.quantity).lstrip('-').partition('.')
        self.quantity = Decimal(parts[0][-7:] + '.' + parts[2][:2].ljust(2, '0'))

        super().save(*args, **kwargs)

    def get_unit_name(self):
        return Ingredient.Unit.units[self.unit][Ingredient.Unit.NAME_KEY]

    def get_unit_symbol(self):
        return Ingredient.Unit.units[self.unit][Ingredient.Unit.SYMBOL_KEY]

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions', related_query_name='instruction')
    text = models.TextField()

    def __str__(self):
        return self.text

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles', related_query_name='profile', primary_key=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    status = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
