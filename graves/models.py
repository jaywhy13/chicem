from django.contrib.gis.db import models
from django.contrib.gis.utils import LayerMapping
from dateutil import parser
from datetime import datetime, timedelta

import os

class Grave(models.Model):
    id = models.IntegerField(primary_key=True)
    ident = models.CharField(max_length=24)
    id_no = models.FloatField()
    id_no_1 = models.IntegerField()
    section = models.CharField(max_length=254)
    row = models.CharField(max_length=254)
    plot = models.CharField(max_length=254)
    area = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    first_name = models.CharField(max_length=254)
    surname = models.CharField(max_length=254)
    given_chin = models.CharField(max_length=254)
    id_1 = models.IntegerField()
    maiden_nam = models.CharField(max_length=254)
    died = models.CharField(max_length=254)
    age = models.CharField(max_length=254)
    book = models.CharField(max_length=254)
    note = models.CharField(max_length=254)
    geom = models.MultiPointField(srid=4326)
    objects = models.GeoManager()

    def get_deceased_date(self):
        if not self.died:
            return None
        
        dt = parser.parse(self.died)
        if dt:
            return dt
        return None
            
    def get_birth_date(self):
        if self.died and self.age:
            dt = parser.parse(self.died)
            if dt:
                birth_date = dt - timedelta(days=int(self.age) * 356)
                return birth_date
        return None
            
    def get_life_duration(self):
        birth_date = self.get_birth_date()
        deceased_date = self.get_deceased_date()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        if birth_date:
            if birth_date.year >= 1900:
                birth_date_str = birth_date.strftime("%b %Y")
            else:
                birth_date_str = "%s %s" % (months[birth_date.month - 1], birth_date.year)

        if deceased_date:
            if deceased_date.year >= 1900:
                deceased_date_str = deceased_date.strftime("%b %Y")
            else:
                deceased_date_str = "%s %s" % (months[deceased_date.month - 1], deceased_date.year)

        if birth_date:
            return "%s - %s" % (birth_date_str, deceased_date_str)
            
        if deceased_date:
            return "Died %s" % deceased_date_str
        
        return "Unknown"
        

# Auto-generated `LayerMapping` dictionary for Grave model
grave_mapping = {
    'ident' : 'IDENT',
    'id_no' : 'ID_NO',
    'id_no_1' : 'ID_No_1',
    'section' : 'Section',
    'row' : 'Row',
    'plot' : 'Plot',
    'area' : 'Area',
    'title' : 'Title',
    'name' : 'Name',
    'first_name' : 'First_Name',
    'surname' : 'Surname',
    'given_chin' : 'Given_Chin',
    'id' : 'ID',
    'id_1' : 'ID_1',
    'maiden_nam' : 'Maiden_Nam',
    'died' : 'Died',
    'age' : 'Age',
    'book' : 'Book',
    'note' : 'Note',
    'geom' : 'MULTIPOINT',
}


def load_graves(verbose=True):
    shp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Graves_WGS84.shp'))
    lm = LayerMapping(Grave,shp_file, grave_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)


class CemeteryBoundary(models.Model):
    id = models.IntegerField(primary_key=True)
    section = models.CharField(max_length=30)
    hotlink = models.CharField(max_length=100)
    area = models.FloatField()
    perimeter = models.FloatField()
    acres = models.FloatField()
    hectares = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for CemeteryBoundary model
cemeteryboundary_mapping = {
    'id' : 'ID',
    'section' : 'SECTION',
    'hotlink' : 'HOTLINK',
    'area' : 'AREA',
    'perimeter' : 'PERIMETER',
    'acres' : 'ACRES',
    'hectares' : 'HECTARES',
    'geom' : 'MULTIPOLYGON',
}


def load_boundaries(verbose=True):
    shp_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/cemetery_boundary_WGS84.shp'))
    lm = LayerMapping(CemeteryBoundary,shp_file, cemeteryboundary_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)
