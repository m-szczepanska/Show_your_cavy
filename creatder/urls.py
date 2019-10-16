from django.urls import path
from creatder.views import (
    creature_list, user_list, create_creature_to_owner, get_own_creatures,
    creature_details, rate_creature)

urlpatterns = [
    path('users/', user_list),
    path('creatures/', creature_list),
    path('creatures/<int:id>/', creature_details),
    path('creatures/<int:creature_id>/rate_creature', rate_creature),
    path('creatures/add_creature/<int:id>/', create_creature_to_owner),
    path('users/<int:id>/creatures/', get_own_creatures)
]
