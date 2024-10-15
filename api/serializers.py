from rest_framework import serializers
from rapihogar.models import Company, Technical


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class TechnicalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technical
        fields = '__all__'
