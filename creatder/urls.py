from django.urls import path
from creatder.views import (
    creature_list, creature_list_paginated, user_list, user_details,
    create_creature, get_user_creatures, creature_details, rate_creature, login,
    register_request_view, register_view, reset_password_view,
    password_reset_request, logout)

urlpatterns = [
    path('users/', user_list),
    path('users/<int:id>/', user_details),
    path('creatures/', creature_list),
    path('creatures/<int:page>/', creature_list_paginated),
    path('creatures/<int:id>/', creature_details),
    path('creatures/<int:id>/rate_creature', rate_creature),
    path('users/<int:user_id>/add_creature/', create_creature),
    path('users/<int:id>/creatures/', get_user_creatures),
    path('login/', login),
    path('register_request/', register_request_view),
    path('register/<uuid:token_uuid>/', register_view),
    path('password_reset_request/', password_reset_request),
    path('password_reset/<uuid:token_uuid>/', reset_password_view),
    path('logout/', logout)
]
