from os.path import basename
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views import *

# Routes
router = routers.SimpleRouter()
router.register(r'pokemons', PokemonViewset, basename='PokemonViewset')
router.register(r'regions', RegionViewset, basename='RegionViewset')
router.register(r'locations', LocationViewset, basename='LocationViewset')
router.register(r'areas', AreaViewset, basename='AreaViewset')

urlpatterns = [
    path(r'', include(router.urls)),
    path('populate/', populate_database, name='populate'),
    path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('pokemons/own/<int:pk>/', PokemonViewset.as_view({'put': 'own', 'patch': 'own', 'delete': 'own'}), name='own_mod'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
