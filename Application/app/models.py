"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Camps(models.Model):
	name = models.TextField()
	capacity = models.IntegerField()
	contact = models.IntegerField()
	lat = models.DecimalField(max_digits=9, decimal_places=6) 
	lon = models.DecimalField(max_digits=9, decimal_places=6)

class Resources(models.Model):
	cid = models.ForeignKey(Camps, on_delete = models.CASCADE)
	resource = models.TextField()
	qty = models.IntegerField()
	unit = models.TextField()

