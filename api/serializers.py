from .models import Location, Pokemon, Area, PokemonUser, Region
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = (
            'id',
            'abilities',
            'capture_rate',
            'color',
            'flavor_text',
            'height',
            'moves',
            'name',
            'sprites',
            'stats',
            'types',
            'weight',
        )


class AreaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id',
            'location',
            'name',
            'pokemon_count',
        )


class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = (
            'id',
            'location',
            'name',
            'pokemons',
        )
                
        
class LocationDetailsSerializer(serializers.ModelSerializer):
    areas = AreaDetailsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'areas',
        )        


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
        )        


class RegionDetailsSerializer(serializers.ModelSerializer):
    locations = LocationListSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = (
            'id',
            'name',
            'locations'
        )


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            'id',
            'name',
        )
        
        
class PokemonUserListSerializer(serializers.ModelSerializer):
    specie = PokemonSerializer(read_only=True)
    
    class Meta:
        model = PokemonUser
        fields = (
            'id',
            'nick_name',
            'is_party_member',
            'specie',
        )
        
class PokemonUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonUser
        fields = (
            'id',
            'nick_name',
            'is_party_member',
            'specie',
        )
        
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user