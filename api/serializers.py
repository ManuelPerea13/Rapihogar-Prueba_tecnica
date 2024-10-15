from rest_framework import serializers
from rapihogar.models import Company, Technical, Pedido


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class TechnicalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technical
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = '__all__'
