from rest_framework import serializers
from kandidat.models import Kandidat

class KandidatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kandidat
        fields = ('id',
                  'Vorname',
                  'Nachname',
                  'geschlecht',
                  'email',
                  'Nummer',
                  'ist_erwachsene',"Beschreibung")