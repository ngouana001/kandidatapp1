from django.db import models

# Create your models here.

class Kandidat(models.Model):
    Vorname = models.CharField(max_length=50, blank=False, default='')
    Nachname= models.CharField(max_length=50, blank=False, default='')
    geschlecht = models.CharField(max_length=10, blank=False, default='')
    email = models.CharField(max_length=200,blank=False, default='')
    Nummer = models.CharField(max_length=50, blank=False, default='')
    Beschreibung = models.CharField(max_length=800,blank=False, default='')
    ist_erwachsene = models.BooleanField(default=False, )

    def __str__(self):
         return self.Vorname