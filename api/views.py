from django.db.models import Sum, Q, Avg, Min, Max
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


class ListTechniciansAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Nombre del técnico para filtrar",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: 'Lista de técnicos con el pago calculado'}
    )
    def get(self, request):
        name_filter = request.query_params.get('name', '')
        if name_filter:
            technicians = Technical.objects.filter(
                Q(full_name__icontains=name_filter)
            )
        else:
            technicians = Technical.objects.all()

        response_data = []

        for technician in technicians:
            total_hours = Pedido.objects.filter(technical=technician).aggregate(total_hours=Sum('hours_worked'))['total_hours'] or 0
            payment = self.calculate_payment(total_hours)
            technician.payment = payment
            technician.save()

            response_data.append({
                'id': technician.id,
                'full_name': technician.full_name,
                'hours worked': total_hours,
                'total charge': payment,
                'quantity_orders': technician.quantity_orders
            })

        return Response(response_data, status=HTTP_200_OK)

    def calculate_payment(self, total_hours):

        if total_hours <= 14:
            hourly_rate = 200
            discount = 0.15
        elif total_hours <= 28:
            hourly_rate = 250
            discount = 0.16
        elif total_hours <= 47:
            hourly_rate = 300
            discount = 0.17
        else:
            hourly_rate = 350
            discount = 0.18

        total_payment = total_hours * hourly_rate
        total_payment -= total_payment * discount

        return total_payment


class ReportAPIView(APIView):

    def get(self, request):
        avg_payment = Technical.objects.aggregate(avg_payment=Avg('payment'))['avg_payment'] or 0
        technicians_below_avg = Technical.objects.filter(payment__lt=avg_payment)
        last_lowest_paid = Technical.objects.filter(payment=Technical.objects.aggregate(min_payment=Min('payment'))['min_payment']).last()
        last_highest_paid = Technical.objects.filter(payment=Technical.objects.aggregate(max_payment=Max('payment'))['max_payment']).last()

        response_data = {
            'avg_payment': avg_payment,
            'technicians_below_avg': [
                {
                    'id': tech.id,
                    'full_name': tech.full_name,
                    'payment': tech.payment
                } for tech in technicians_below_avg
            ],
            'last_lowest_paid': {
                'id': last_lowest_paid.id,
                'full_name': last_lowest_paid.full_name,
                'payment': last_lowest_paid.payment
            } if last_lowest_paid else None,
            'last_highest_paid': {
                'id': last_highest_paid.id,
                'full_name': last_highest_paid.full_name,
                'payment': last_highest_paid.payment
            } if last_highest_paid else None
        }

        return Response(response_data, status=HTTP_200_OK)
