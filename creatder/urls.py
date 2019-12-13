from django.urls import path
from creatder.views import (
    creature_list, user_list, user_details,
    create_creature, get_user_creatures, creature_details, rate_creature,
    login, register_request_view, register_view, reset_password_view,
    creature_list_paginated, password_reset_request, logout, FileUploadView,
    FileUploadDetails, user_ratings, search_creature)


urlpatterns = [
    path('users/', user_list),
    path('users/<int:id>/', user_details),
    path('users/<int:id>/creatures/', get_user_creatures),
    path('users/<int:id>/ratings/', user_ratings),
    path('users/<int:user_id>/add_creature/', create_creature),
    path('creatures/', creature_list),
    path('creatures_all/<int:page>/', creature_list_paginated),
    path('creatures/<int:id>/', creature_details),
    path('creatures/<int:id>/rate_creature/', rate_creature),
    path('creatures/search/', search_creature),
    path('login/', login),
    path('register_request/', register_request_view),
    path('register/<uuid:token_uuid>/', register_view),
    path('password_reset_request/', password_reset_request),
    path('password_reset/<uuid:token_uuid>/', reset_password_view),
    path('logout/', logout),
    path('creatures/<int:creature_id>/photos/', FileUploadView.as_view()),
    path('creatures/<int:creature_id>/photos/<int:id>/', FileUploadDetails.as_view()),
]
