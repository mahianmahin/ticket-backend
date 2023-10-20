from rest_framework import serializers

from .models import *


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ('date',)


class BusPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPackages
        fields = "__all__"

class MuseumPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuseumPackages
        fields = "__all__"

    def to_representation(self, instance):
        current_object = self.instance

        date_list = []

        serialized_dates = DateSerializer(current_object.dates, many=True)
        
        for item in serialized_dates.data:
            date_list.append(item['date'])

        data = super().to_representation(instance)
        data['dates'] = date_list

        return data