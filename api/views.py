from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rapihogar.models import Company, Technical, Pedido, User, Scheme
from .serializers import CompanySerializer, TechnicalSerializer

import random

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()


class TechnicalViewSet(viewsets.ModelViewSet):
    serializer_class = TechnicalSerializer
    queryset = Technical.objects.filter()


class GenerateOrdersAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('N', openapi.IN_QUERY, description="Número de pedidos a generar", type=openapi.TYPE_INTEGER, required=True)
        ],
        responses={200: 'Pedidos generados correctamente'}
    )
    def post(self, request):
        n = request.query_params.get('N')

        if not n.isdigit():
            return Response({"error": "N debe ser un número entero"}, status=HTTP_400_BAD_REQUEST)

        n = int(n)

        if n < 1 or n > 100:
            return Response({"error": "N debe estar entre 1 y 100"}, status=HTTP_400_BAD_REQUEST)

        clients = list(User.objects.all())
        technicians = list(Technical.objects.all())

        if not technicians or not clients:
            return Response({"error": "Debe haber al menos un Técnico y un Cliente en la base de datos"}, status=HTTP_400_BAD_REQUEST)

        for _ in range(n):
            client = random.choice(clients)
            technical = random.choice(technicians)
            hours_worked = random.randint(1, 50)
            scheme = Scheme.objects.get(id=1)

            Pedido.objects.create(
                client=client,
                technical=technical,
                hours_worked=hours_worked,
                type_request=1,
                scheme=scheme
            )

        return Response({"success": f"Se han generado {n} pedidos correctamente"}, status=HTTP_200_OK)
