from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.fields import BooleanField

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Pokemon(BaseModel):
    abilities = ArrayField(models.CharField(max_length=200), blank=True)
    capture_rate = models.DecimalField(max_digits=5, decimal_places=1)
    color = models.CharField(max_length=60)
    flavor_text = models.TextField()
    height = models.IntegerField(default=0)
    moves = ArrayField(models.CharField(max_length=200), blank=True)
    name = models.CharField(max_length=100)
    stats = JSONField()
    sprites = JSONField()
    types = ArrayField(models.CharField(max_length=200), blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        db_table = 'pokemon'       
  
  
class Region(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'region' 

class Location(BaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='locations', on_delete=models.CASCADE)

    class Meta:
        db_table = 'location' 
        

class Area(BaseModel):
    location = models.ForeignKey(Location, related_name='areas', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pokemons = JSONField()
    pokemon_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'area' 
        

class PokemonUser(BaseModel):
    nick_name = models.CharField(max_length=100)
    is_party_member = BooleanField(default=False)
    specie = models.ForeignKey(Pokemon, related_name='specie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'pokemon_user' 