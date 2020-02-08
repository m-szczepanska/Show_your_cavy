from datetime import datetime, timezone
from sys import exit
from uuid import uuid4

from django.test import TestCase

from creatder.models import (User, Creature, Review,
    Token, PasswordResetToken, CreateAccountToken, File)
from tests.fixtures import gen_user, gen_creature


class TestUserModel(TestCase):

    def setUp(self):
        self.users = [
            gen_user(
                name="John",
                login="Doe",
                email="john@doe.test.com",
            ),
            gen_user(
                name="Johnny",
                login="Does",
                email="johnny@does.test.com",
            ),
            gen_user(
                name="Jon",
                login="Doy",
                email="jon@doy.test.com",
            )
        ]
        self.creatures = [
            gen_creature(
                name='Pig',
                age='5',
                sex='Male',
                breed='Other',
                color_pattern='Mix',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='Piggu',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            )]

        self.review_1 = Review(
            creature = self.creatures[0],
            user = self.users[1],
            comment = 'Total potato',
            rating = 4
        )
        self.review_2 = Review(
            creature = self.creatures[1],
            user = self.users[1],
            comment = 'A real beauty',
            rating = 5)

        self.review_1.save()
        self.review_2.save()


    def test_check_password_correct_password(self):
        result = self.users[0].check_password('P@ssw0rd!')

        self.assertTrue(result)

    def test_user_creatures_correct(self):
        user = self.users[0]
        result = user.creatures

        self.assertEqual(len(result), len(self.creatures))
        for creature in self.creatures:
            assert(creature in result)

    def test_user_get_user_ratings_correct(self):
        user = self.users[1]
        reviews = [self.review_1, self.review_2]
        result = user.get_user_ratings

        self.assertEqual(len(reviews), len(result))
        for review in reviews:
            assert(review in result)


class TestCreatureModel(TestCase):

    def setUp(self):
        self.users = [
            gen_user(
                name="John",
                login="Doe",
                email="john@doe.test.com",
            ),
            gen_user(
                name="Johnny",
                login="Does",
                email="johnny@does.test.com",
            ),
            gen_user(
                name="Jon",
                login="Doy",
                email="jon@doy.test.com",
            )
        ]
        self.creatures = [
            gen_creature(
                name='Pig',
                age='5',
                sex='Male',
                breed='Other',
                color_pattern='Mix',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='Piggu',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            )]

        self.review_1 = Review(
            creature = self.creatures[0],
            user = self.users[1],
            comment = 'Total potato',
            rating = 4
        )
        self.review_2 = Review(
            creature = self.creatures[0],
            user = self.users[2],
            comment = 'A real beauty',
            rating = 5
        )

        self.review_1.save()
        self.review_2.save()

        self.photo_1 = File(
            file = '/Users/marsza/workspace/media/szczesliwy_opos.png',
            creature = self.creatures[0]
        )
        self.photo_2 = File(
            file = '/Users/marsza/workspace/media/photo_info.png',
            creature = self.creatures[0]
        )
        self.photo_1.save()
        self.photo_2.save()


    def test_average_rating_correct(self):
        expected_rating = (4 + 5) /2
        creature = self.creatures[0]
        result = creature.average_rating

        self.assertEqual(expected_rating, result)

    def test_creature_photos_correct(self):
        photos = [self.photo_1, self.photo_2]
        creature = self.creatures[0]
        result = creature.creature_photos
        # import pdb; pdb.set_trace()

        self.assertEqual(len(photos), len(result))
        for photo in photos:
            assert(photo in result)

    def test_creature_card_photos_correct(self):
        photo = self.photo_1
        creature = self.creatures[0]
        result = creature.creature_card_photo

        self.assertEqual(photo, result)


class TestCreateAccountToken(TestCase):

    def test_create_account_token_is_valid_true(self):
        self.account_token = CreateAccountToken(
            email="john@doe.test.com",
            created_at=datetime.now(timezone.utc)
        )
        self.account_token.save()
        token = self.account_token

        self.assertTrue(token.is_valid)

    def test_create_account_token_is_valid_false_used(self):
        self.account_token = CreateAccountToken(
            email="john@doe.test.com",
            created_at=datetime.now(timezone.utc),
            was_used = True
        )
        self.account_token.save()
        token = self.account_token

        self.assertFalse(token.is_valid)

    def test_create_account_token_is_valid_false_timedelta(self):
        self.account_token = CreateAccountToken(
            email="john@doe.test.com",
            created_at=datetime(2019, 12, 4, tzinfo=timezone.utc),
        )
        self.account_token.save()
        token = self.account_token

        self.assertFalse(token.is_valid)

    def test_create_account_token_is_valid_double_false(self):
        self.account_token = CreateAccountToken(
            email="john@doe.test.com",
            created_at=datetime(2019, 12, 4, tzinfo=timezone.utc),
            was_used = True
        )
        self.account_token.save()
        token = self.account_token

        self.assertFalse(token.is_valid)


class TestPasswordResetToken(TestCase):
    def setUp(self):
        self.users = [
            gen_user(
                name="John",
                login="Doe",
                email="john@doe.test.com",
                ),
                gen_user(
                name="Johnny",
                login="Does",
                email="johnny@does.test.com",
                ),
                gen_user(
                name="Jon",
                login="Doy",
                email="jon@doy.test.com",
                )
        ]


    def test_password_reset_token_is_valid_true(self):
        self.password_token = PasswordResetToken(
            user=self.users[0],
            created_at=datetime.now(timezone.utc)
        )
        self.password_token.save()
        token = self.password_token

        self.assertTrue(token.is_valid)

    def test_password_reset_token_is_valid_false_used(self):
        self.password_token = PasswordResetToken(
            user=self.users[0],
            created_at=datetime.now(timezone.utc),
            was_used = True
        )
        self.password_token.save()
        token = self.password_token

        self.assertFalse(token.is_valid)

    def test_password_reset_token_is_valid_false_timedelta(self):
        self.password_token = PasswordResetToken(
            user=self.users[0],
            created_at=datetime(2019, 12, 12, tzinfo=timezone.utc),
        )
        self.password_token.save()
        token = self.password_token

        self.assertFalse(token.is_valid)

    def test_password_reset_token_is_valid_double_false(self):
        self.password_token = PasswordResetToken(
            user=self.users[0],
            created_at=datetime(2019, 12, 4, tzinfo=timezone.utc),
            was_used = True
        )
        self.password_token.save()
        token = self.password_token

        self.assertFalse(token.is_valid)
