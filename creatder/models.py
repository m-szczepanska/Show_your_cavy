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

    # TODO: Add validation when creating user
    def set_password(self, password_plaintext):
        password_hashed = make_password(password_plaintext)
        self._password = password_hashed
        self.save()

    # I would change this to 'creatures' since it will be used like
    # user.creatures instead of user.get_own_creatures()
    @property
    def creatures(self):
        creatures = Creature.objects.filter(owner__id=self.id).all()
        return creatures

    @property
    def get_user_ratings(self):
        ratings = Review.objects.filter(user__id=self.id).all()
        return ratings


class Creature(models.Model):
    BREED = [
        ('Other', 'Other'),
        ('American', 'American'),
        ('Abyssinian', 'Abyssinian'),
        ('Hairless', 'Hairless'),
        ('Himalayan', 'Himalayan'),
        ('Peruvian', 'Peruvian'),
        ('Rex', 'Rex'),
        ('Silkie', 'Silkie'),
        ('Teddy', 'Teddy'),
        ('White-crested', 'White-crested')
    ]
    COLOR_AND_PATTERN = [
        ('Self-Black', 'Self-Black'),
        ('Self-White', 'Self-White'),
        ('Self-Red', 'Self-Red'),
        ('Self-Cream', 'Self-Cream'),
        ('Agouti-Chocolate', 'Agouti-Chocolate'),
        ('Agouti-Golde', 'Agouti-Golde'),
        ('Agouti-Silver', 'Agouti-Silver'),
        ('Agouti-Cream', 'Agouti-Cream'),
        ('White-Black', 'White-Black'),
        ('White-Red', 'White-Red'),
        ('Red-Black', 'Red-Black'),
        ('White-Cream', 'White-Cream'),
        ('Brindle', 'Brindle'),
        ('Mix', 'Mix'),
        ('Albino', 'Albino')
    ]
    SEX = [('Female', 'Female'), ('Male', 'Male'), ('Not sure', 'Not sure')]
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    sex = models.CharField(max_length=8, choices=SEX, default='Female')
    breed = models.CharField(max_length=15, choices=BREED, default='Other')
    color_pattern = models.CharField(
        max_length=20,
        choices=COLOR_AND_PATTERN,
        default='Mix'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    crossed_rainbow_bridge = models.BooleanField(default=False, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.name

    @property
    def average_rating(self):
        # TODO: Round to 2 decimal numbers
        all_reviews = Review.objects.filter(creature__id=self.id)
        ratings_count = all_reviews.count()
        # Could also be done with aggregate: https://stackoverflow.com/a/8616400
        ratings_sum = 0
        for obj in all_reviews:
            ratings_sum += obj.rating
        if ratings_count != 0:
            result = ratings_sum / ratings_count
        else:
            result = 0
        return result

    @property
    def creature_photos(self):
        all_photos = File.objects.filter(creature__id=self.id)
        return all_photos

    @property
    def creature_card_photo(self):
        card_photo = File.objects.filter(creature__id=self.id).first()
        return card_photo


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    # creature and user should be "unique together"; truncate reviews before
    # migrating!
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    uuid = models.CharField(max_length=200, default=uuid4)
    is_expired = models.BooleanField(default=False)

    # This is an example of a FactoryMethod design pattern
    # @classmethod
    # def create(cls, user_id, is_expired):
    #     instance = cls(uuid=uuid4(), user_id=user_id)
    #     instance.save()
    #     return instance


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200, default=uuid4)
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    was_used = models.BooleanField(default=False)

    @property
    def is_valid(self):
        timedelta = datetime.now(timezone.utc) - self.created_at
        return not self.was_used and timedelta.days < 1


class CreateAccountToken(models.Model):
    email = models.EmailField(max_length=254)
    uuid = models.CharField(max_length=200, default=uuid4)
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    was_used = models.BooleanField(default=False)

    @property
    def is_valid(self):
        timedelta = datetime.now(timezone.utc) - self.created_at
        return not self.was_used and timedelta.days < 1


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
