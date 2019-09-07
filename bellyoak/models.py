from django.db import models
from django.template.defaultfilters import slugify

from decimal import Decimal

# Research integer and decimal validation

class Recipe(models.Model):
    NONE = 'NONE'
    VEGETARIAN = 'VEGETARIAN'
    VEGAN = 'VEGAN'

    DIETS = [
        (NONE, 'None'),
        (VEGETARIAN, 'Vegetarian'),
        (VEGAN, 'Vegan'),
    ]

    # Add course, cuisine, publish/update dates, tags

    title = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='recipe_images', blank=True)
    description = models.TextField(blank=True)
    # preparation_time = models.DurationField(blank=True, null=True)
    # cooking_time = models.DurationField(blank=True, null=True)
    servings = models.IntegerField(default=1)
    diet = models.CharField(max_length=255, choices=DIETS, default=NONE)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=63)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):        
        if self.likes < 0:
            self.likes = 0

        if self.views < 0:
            self.views = 0

        self.slug = slugify(self.title)

        super().save(*args, **kwargs)

class Ingredient(models.Model):
    NONE = 'NONE'
    GRAM = 'GRAM'
    KILOGRAM = 'KILOGRAM'
    MILLILITRE = 'MILLILITRE'
    LITRE = 'LITRE'
    TEASPOON = 'TEASPOON'
    TABLESPOON = 'TABLESPOON'
    CUP = 'CUP'
    PINT = 'PINT'

    # Add length, more units, imperial

    UNITS = [
        (NONE, 'None'),
        ('Mass', (
                (GRAM, 'g (grams)'),
                (KILOGRAM, 'kg (kilograms)'),
            )
        ),
        ('Volume', (
                (MILLILITRE, 'ml (millilitres)'),
                (LITRE, 'l (litres)'),
                (TEASPOON, 'tsp (teaspoons)'),
                (TABLESPOON, 'tbsp (tablespoons)'),
                (CUP, 'cup (cups)'),
                (PINT, 'pt. (pints)'),
            )
        ),
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal())
    unit = models.CharField(max_length=255, choices=UNITS, default=NONE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if float(self.quantity) < 0:
            self.quantity = Decimal('-' + str(self.quantity))

        super().save(*args, **kwargs)

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    index = models.IntegerField(default=0)
    text = models.TextField()

    def __str__(self):
        return self.index

    def save(self, *args, **kwargs):
        # Set index 1 higher than previous instruction for this recipe, or set index to 1 if no previous instruction
        # Unsaved instruction has default index of 0
        if self.index == 0:
            try:
                last_instruction = Instruction.objects.filter(recipe__exact=self.recipe).order_by('-index')[0]
                self.index = last_instruction.index + 1
            except IndexError:
                self.index = 1

        super().save(*args, **kwargs)
