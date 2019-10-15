from django.urls import path
from creatder.views import (
    creature_list, user_list, create_creature_to_owner, get_own_creatures)

urlpatterns = [
    path('users/', user_list),
    path('creatures/', creature_list),
    path('creatures/add_creature/<int:id>/', create_creature_to_owner),
    path('users/<int:id>/creatures/', get_own_creatures)
]
