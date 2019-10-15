from datetime import datetime, timezone
from uuid import uuid4

from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class User(models.Model):
    """ Model containing four basic informations from users about themselves.
    Args:
        name - string; max length 255 chars
        login - string; max length 50 chars
        email - unique string; max length 254 chars
        _password - hashed string
        about_myself - short description, string; max length 255 chars
    """
    name = models.CharField(max_length=255, blank=False)
    login = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    _password = models.CharField(max_length=255, blank=False)  # hashed
    about_myself = models.CharField(max_length=255, blank=True)

    def check_password(self, password_plaintext):
        return check_password(password_plaintext, self._password)

    # TODO: Add validation when creating player
    def set_password(self, password_plaintext):
        password_hashed = make_password(password_plaintext)
        self._password = password_hashed
        self.save()

    # I would change this to 'creatures' since it will be used like
    # user.creatures instead of user.get_own_creatures()
    @property
    def get_own_creatures(self):
        creatures = Creature.objects.filter(owner__id=self.id).all()
        return creatures


class Creature(models.Model):
    BREED = [
        ('OT', 'Other'),
        ('AM', 'American'),
        ('AB', 'Abyssinian'),
        ('HR', 'Hairless'),
        ('HI', 'Himalayan'),
        ('PR', 'Peruvian'),
        ('RX', 'Rex'),
        ('SL', 'Silkie'),
        ('TD', 'Teddy'),
        ('WD', 'White-crested')
    ]
    COLOR_AND_PATTERN = [
        ('BL', 'Self-Black'),
        ('WH', 'Self-White'),
        ('RD', 'Self-Red'),
        ('CR', 'Self-Cream'),
        ('CH', 'Agouti-Chocolate'),
        ('AG', 'Agouti-Golde'),
        ('AV', 'Agouti-Silver'),
        ('AC', 'Agouti-Cream'),
        ('WB', 'White-black'),
        ('WR', 'White-red'),
        ('SB', 'Red-black'),
        ('WC', 'White-cream'),
        ('BR', 'Brindle'),
        ('MX', 'Mix'),
        ('AL', 'Albino')
    ]
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    breed = models.CharField(max_length=2, choices=BREED, default='OT')
    color_pattern = models.CharField(
        max_length=2,
        choices=COLOR_AND_PATTERN,
        default='MX'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def average_rating(self):
        all_reviews = Review.objects.filter(creature__id=self.id)
        ratings_count = all_reviews.count()
        # Could also be done with aggregate: https://stackoverflow.com/a/8616400
        ratings_sum = 0
        for obj in all_reviews:
            ratings_sum += obj.rating
        return ratings_sum / ratings_count


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
