from rest_framework import serializers

class ScrapeSerializer(serializers.Serializer):
    url = serializers.URLField()  
        

