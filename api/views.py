# Create your views here.
import os
import json
from django.conf import settings
from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .utils import read_json
from .models import Location, Pokemon, Area, Region
from django.contrib.auth.models import User
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action



def populate_database(request):
    root_path = settings.STATIC_ROOT
    
    pokemon_data = read_json(os.path.join(root_path, 'pokemons.json'))
    region_data = read_json(os.path.join(root_path, 'regions.json'))
    location_data = read_json(os.path.join(root_path, 'locations.json'))
    area_data = read_json(os.path.join(root_path, 'areas.json'))
   
    if not Pokemon.objects.all():
        Pokemon.objects.bulk_create([Pokemon(**{
                'name': pokemon['name'],
                'abilities': pokemon['abilities'],
                'capture_rate': pokemon['capture_rate'],
                'color': pokemon['color'],
                'flavor_text': pokemon['flavor_text'],
                'height': pokemon['height'],
                'moves': pokemon['moves'],
                'types': pokemon['types'],
                'stats': pokemon['stats'],
                'sprites': pokemon['sprites'],
                'weight': pokemon['weight'],
        }) for pokemon in pokemon_data['data']])
    
    for area in area_data['data']:
        area['pokemons'] = list(
            Pokemon.objects.filter(
            name__in=[each_string.capitalize() 
            for each_string in area['pokemons']]).values('id', 'name', 'sprites')
        )
        
        
    if not Region.objects.all():
        Region.objects.bulk_create([Region(**{
                'name': region['name'],
        }) for region in region_data['data']])
    
    
    if not Location.objects.all() and Region.objects.all():
        Location.objects.bulk_create([Location(**{
                'name': location['name'],
                'region': Region.objects.get(name=location['region']),
        }) for location in location_data['data']])    
        
            
    if not Area.objects.all() and Location.objects.all():
        Area.objects.bulk_create([Area(**{
                'location': Location.objects.get(name=area['location']),
                'name': area['name'],
                'pokemons': area['pokemons'],
                'pokemon_count': len(area['pokemons']),
        }) for area in area_data['data']])
    
    result = {
        "Pokemons Inserted": Pokemon.objects.count(),
        "Regions Inserted": Region.objects.count(),
        "Locations Inserted": Location.objects.count(),
        "Areas Inserted": Area.objects.count(),
    }
    return JsonResponse(result)


class PokemonViewset(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post', 'get', 'put', 'patch', 'delete'])
    def own(self, request, pk=None):
        if request.method == 'GET':
            serializer = PokemonUserListSerializer(PokemonUser.objects.filter(user=self.request.user), many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = PokemonUserDetailsSerializer(data=request.data)
            party_members = PokemonUser.objects.filter(is_party_member=True).count()
            if serializer.is_valid():
                if request.data['is_party_member'] and party_members == 6:
                    return Response({'party_members_errors': 'You can only have 6 Pokemons in your party.'},
                                status=status.HTTP_400_BAD_REQUEST)
                specie = Pokemon.objects.get(pk=request.data['specie'])
                serializer.save(user=self.request.user, specie=specie)
                return Response(serializer.data)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        elif request.method in ['PUT', 'PATCH']:
            pokemon = PokemonUser.objects.get(pk=pk)
            pokemon.nick_name = request.data['nick_name']
            pokemon.save(update_fields=['nick_name'])
            serializer = PokemonUserDetailsSerializer(pokemon)
            return Response(serializer.data)
        else:
            pokemon = PokemonUser.objects.get(pk=pk)
            pokemon.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'], url_path=r'own/swap')
    def swap(self, request):
        party_members = PokemonUser.objects.filter(is_party_member=True).count()

        if party_members == 6 and request.data['entering_the_party'] and not request.data['leaving_the_party']:
                return Response({'party_members_errors': 'You can only have 6 Pokemons in your party.'},
                            status=status.HTTP_400_BAD_REQUEST)
                
        if request.data['entering_the_party']:
            pokemon = PokemonUser.objects.filter(user=self.request.user).get(pk=request.data['entering_the_party'])
            pokemon.is_party_member = True
            pokemon.save(update_fields=['is_party_member'])
                
            
        if request.data['leaving_the_party']:
            pokemon = PokemonUser.objects.filter(user=self.request.user).get(pk=request.data['leaving_the_party'])
            pokemon.is_party_member = False
            pokemon.save(update_fields=['is_party_member'])
            
        party = PokemonUser.objects.filter(user=self.request.user, is_party_member=True)
            
            
        serializer = PokemonUserListSerializer(party, many=True)
            
        return Response(serializer.data)
        
    
    @action(detail=False, methods=['get'], url_path=r'own/party')
    def pokemon_party(self, request):
        pokemon = PokemonUser.objects.filter(user=self.request.user, is_party_member=True)
        serializer = PokemonUserListSerializer(pokemon, many=True)
        return Response(serializer.data)
    
    
    
    
class RegionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = Region.objects.all()
        serializer = RegionListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Region.objects.all()
        region = get_object_or_404(queryset, pk=pk)
        serializer = RegionDetailsSerializer(region)
        return Response(serializer.data)
    
    
class LocationViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = Location.objects.all()
        serializer = LocationListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Location.objects.all()
        location = get_object_or_404(queryset, pk=pk)
        serializer = LocationDetailsSerializer(location)
        return Response(serializer.data)


class AreaViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = Area.objects.all()
        serializer = AreaListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Area.objects.all()
        area = get_object_or_404(queryset, pk=pk)
        serializer = AreaListSerializer(area)
        return Response(serializer.data)
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
