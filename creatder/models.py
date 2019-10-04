from django.contrib.auth.hashers import check_password, make_password
from django.db import models


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
    ('Self',
        ('BL', 'Black'),
        ('WH', 'White'),
        ('RD', 'Red'),
        ('CR', 'Cream')
    ),
    ('Agouti',
        ('CH', 'Chocolate'),
        ('GD', 'Golde'),
        ('SV', 'Silver'),
        ('CR', 'Cream')
    ),
    ('Dutch Bicolour and Tortoiseshell',
        ('WB', 'White-black'),
        ('WR', 'White-red'),
        ('SB', 'Red-black'),
        ('WC', 'White-cream')
    ),
    ('BR', 'Brindle'),
    ('MX', 'Mix'),
    ('AL', 'Albino')
    ]
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, choices=BREED, default='OT')
    color_pattern = models.CharField(
        max_length=50,
        choices=COLOR_AND_PATTERN,
        default='MX'
    )

    def __unicode__(self):
        return self.name

    # def average_rating(self):
    #     all_ratings = map(lambda x: x.rating, self.review_set.all())
    #     return np.mean(all_ratings)




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
    login = models.CharField(max_length=50, blank=False)
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


class Review(models.Model):
    RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    )
    creature = models.ForeignKey(Creature.id)
    pub_date = models.DateTimeField('date published')
    user_name = models.ForeignKey(User.id)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
