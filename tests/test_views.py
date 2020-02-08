import json
from unittest.mock import MagicMock, patch

from rest_framework import status
from django.test import TestCase, Client
from django.db.utils import IntegrityError

from creatder.models import (User, Creature, Review,
    Token, PasswordResetToken, CreateAccountToken, File)
from creatder.serializers import (GetCreatureSerializer,
    CreateCreatureSerializer, GetUserSerializer, CreateUserSerializer,
    UpdateUserSerializer, RateCreatureSerializer,GetUserRatingsSerializer,
    UpdateCreatureSerializer, RegisterTokenSerializer, RegisterRequestSerializer,
    TokenSerializer, LoginSerializer, PasswordResetRequestSerializer,
    PasswordResetTokenSerializer, PasswordUserSerializer,
    FileSerializer, SearchCreatureSerializer)
from creatder.services import check_token_validity

from tests.fixtures import gen_user, gen_creature

client = Client()
BASE_URL='//127.0.0.1:8000/creatder'


class TestPlayerDetailsViews(TestCase):

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
                name='a',
                age='5',
                sex='Male',
                breed='Other',
                color_pattern='Mix',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='b',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='c',
                age='5',
                sex='Male',
                breed='Other',
                color_pattern='Mix',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='d',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='e',
                age='5',
                sex='Male',
                breed='Other',
                color_pattern='Mix',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='f',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='g',
                age='5',
                sex='Male',
                breed='Other',
                color_pattern='Mix',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='h',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='i',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            ),
            gen_creature(
                name='j',
                age='1',
                sex='Male',
                breed='Other',
                color_pattern='Albino',
                crossed_rainbow_bridge=False,
                owner = self.users[0]
            )
            ]
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


    def test_get_all_creatures_ok(self):
        response = client.get(
        f'{BASE_URL}/creatures/')
        expected = GetCreatureSerializer(self.creatures, many=True).data

        self.assertEqual(len(response.json()), len(expected))
        for creature in response.json():
            assert(creature in expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_creatures_one_pig_ok(self):
        response = client.get(
            f'{BASE_URL}/creatures/10/')
        expected = GetCreatureSerializer(self.creatures[9]).data

        self.assertEqual(len(response.json()), len(expected))
        for creature in response.json():
            assert(creature in expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creature_list_paginated_ok(self):
        response = client.get(
            f'{BASE_URL}/creatures_all/1/')
        expected = GetCreatureSerializer(self.creatures[1:], many=True).data

        self.assertEqual(len(response.json()['objects']), len(expected), 9)
        for creature in response.json()['objects']:
            assert(creature in expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creature_list_paginated_404(self):
        response = client.get(
            f'{BASE_URL}/creatures_all/10/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list_get_ok(self):
        response = client.get(
            f'{BASE_URL}/users/')
        expected = GetUserSerializer(self.users, many=True).data

        self.assertEqual(len(response.json()), len(expected))
        for user in response.json():
            assert(user in expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user_list_ok(self):
        response = client.get(
            f'{BASE_URL}/users/')
        expected = GetUserSerializer(self.users, many=True).data

        self.assertEqual(len(response.json()), len(expected))
        for user in response.json():
            assert(user in expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_post_ok(self):
        payload = {
            'name': 'test_user',
            'login': 'test_user',
            'email': 'test_user@test.email.com',
            'about_myself': '',
            'password': 'test_user1',
            'password_repeat': 'test_user1'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()

        self.assertEqual(resp_json['name'], payload['name'])
        self.assertEqual(resp_json['login'], payload['login'])
        self.assertEqual(resp_json['email'], payload['email'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_post_different_passwords(self):
        payload = {
            'name': 'test_user',
            'login': 'test_user',
            'email': 'test_user@test.email.com',
            'about_myself': '',
            'password': 'test_user1',
            'password_repeat': 'test_user2'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        response_text = {'non_field_errors': ['Passwords did not match.']}

        self.assertEqual(resp_json, response_text)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_passwords_too_short(self):
        payload = {
            'name': 'test_user',
            'login': 'test_user',
            'email': 'test_user@test.email.com',
            'about_myself': '',
            'password': 'test',
            'password_repeat': 'test'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        response_text = {
            'non_field_errors': ['Passwords must have at least 8 characters.']
        }

        self.assertEqual(resp_json, response_text)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_no_digit_passwords(self):
        payload = {
            'name': 'test_user',
            'login': 'test_user',
            'email': 'test_user@test.email.com',
            'about_myself': '',
            'password': 'testuser',
            'password_repeat': 'testuser'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        response_text = {
            'non_field_errors': ['Password must contain at least 1 digit.']
        }

        self.assertEqual(resp_json, response_text)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_bad_email_syntax(self):
        payload = {
            'name': 'test_user',
            'login': 'test_user',
            'email': 'test_usertest.email.com',
            'about_myself': '',
            'password': 'testuser',
            'password_repeat': 'testuser'
        }
        response = client.post(
            f'{BASE_URL}/users/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_json = response.json()
        response_text = {
            'email': ['Enter a valid email address.']
        }

        self.assertEqual(resp_json, response_text)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_post_duplicate_email(self):
        player_dicts = [
            {
                'name': 'test_user',
                'login': 'test_user',
                'email': 'test_usertest.email.com',
                'about_myself': '',
                'password': 'testuser1',
                'password_repeat': 'testuser1'
            },
            {
                'name': 'user_test',
                'login': 'user_test',
                'email': 'test_usertest.email.com',
                'about_myself': '',
                'password': 'user_test1',
                'password_repeat': 'user_test1'
            }
        ]
        for elem in player_dicts:
            response = client.post(
                f'{BASE_URL}/users/',
                data=json.dumps(elem),
                content_type='application/json')
        expected = {
            'non_field_errors': ['User with this email already exists.']}

        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
