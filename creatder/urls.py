from django.urls import path
from creatder.views import (
    creature_list, user_list, create_creature_to_owner, creatures,
    creature_details, rate_creature, login, register_request_view,
    register_view, reset_password_view, password_reset_request, logout)

urlpatterns = [
    path('users/', user_list),
    path('creatures/', creature_list),
    path('creatures/<int:id>/', creature_details),
    path('creatures/<int:creature_id>/rate_creature', rate_creature),
    path('creatures/add_creature/<int:id>/', create_creature_to_owner),
    path('users/<int:id>/creatures/', creatures),
    path('login/', login),
    path('register_request/', register_request_view),
    path('register/<uuid:token_uuid>/', register_view),
    path('password_reset_request/', password_reset_request),
    path('password_reset/<uuid:token_uuid>/', reset_password_view),
    path('logout/', logout)
]
