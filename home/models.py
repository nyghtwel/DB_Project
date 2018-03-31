from django.db import models
from datetime import datetime
# Create your models here.

# Create Users
class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_lenght=50)
    email = models.CharField(max_length=20)
    organization = models.CharField(blank=True, null=True, max_length=20)
    job_title = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        managed = True 
        db_table = 'user'

# Create query 
class Query(models.Model):
    query_ID = models.BigIntegerField(primary_key=True)
    domain = models.CharField(blank=True, null=True, max_length=20)
    indicator = models.CharField(blank=True, null=True, max_length=20)
    location = models.CharField(blank=True, null=True, max_length=20)
    population = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return self.query_ID

    class Meta:
        managed = True 
        db_table = 'query' 

class Write(mdoels.Model):
    username = models.ForeignKey(Users)
    query_ID = models.ForeignKey(Query)
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        managed = True 
        db_table = 'write'

class Health_Domain(models.Model):
    domain_ID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(blank=True, null=True, max_length=20)  

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'health_table'

class Chronic_Disease_Indicator(models.Model):
    indicator_ID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(blank=True, null=True, max_length=20)
    year_start = models.BigIntegerField(blank=True, null=True)
    year_end = models.BigIntegerField(blank=True, null=True)
    # domain_ID = models.ForeignKey(Health_Domain) 
    domain_ID = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return self.indicator_ID

    class Meta:
        managed = True
        db_table = 'chronic_disease_indicator'
    
class Location(models.Model):
    location_ID = models.BigIntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=20)
    abbreviation = models.CharField(blank=True, null=True, max_length=20)
    lat_long_pair = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        managed = True 
        db_table = 'location'

class Population(models.Model):
    population_ID = models.CharField(primary_key=True, max_length=20)
    gender = models.CharField(blank=True, null=True, max_length=10)
    race = models.CharField(blank=True, null=True, max_length=10)
    location_ID = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.population_ID

    class Meta:
        managed = True
        db_table = 'population'

class Indicator_Estimate(models.Model):
    data_value = models.FloatField(blank=True, null=True)
    data_unit = models.CharField(blank=True, null=True, max_length=20)
    data_value_type = models.CharField(blank=True, null=True, max_length=20)
    confidence_interval = models.CharField(blank=True, null=True, max_length=20)
    data_source = models.CharField(blank=True, null=True, max_length=20)
    indicator_ID = models.ForeignKey(Indicator_Estimate)
    location_ID = models.ForeignKey(Location)

    class Meta:
        managed = True 
        db_table = 'indicator_estimate'


