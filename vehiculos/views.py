from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Vehiculo, Mantenimiento, CompraVehiculo, Accesorio, Marca, User, Perfil
from .serializers import VehiculoSerializer, MantenimientoSerializer, CompraVehiculoSerializer, AccesorioSerializer, MarcaSerializer, UsuarioSerializer, PerfilSerializer

#Lista de Vehiculos (GET y POST)
#class VehiculoListAPIView(APIView):
#    def get(self, request):
#        vehiculos = Vehiculo.objects.all()
#        serializer = VehiculoSerializer(vehiculos, many=True)
#        return Response(serializer.data)

#    def post(self, request):
#        serializer = VehiculoSerializer(data=request.data)
#        serializer.is_valid()
#        serializer.save()
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Detalle de Vehiculo (GET)
#class VehiculoDetailView(APIView):
#    def get(self, request, pk):
#        try:
#            vehiculo = Vehiculo.objects.get(pk=pk)
#        except Vehiculo.DoesNotExist:
#            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
#        
#        serializer = VehiculoSerializer(vehiculo)
#        return Response(serializer.data)
#    
#    def put(self, request, pk):
#       vehiculo = get_object_or_404(Vehiculo, pk=pk)
#        serializer = VehiculoSerializer(vehiculo, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def patch(self, request, pk):
#        vehiculo = get_object_or_404(Vehiculo, pk=pk)
#        serializer = VehiculoSerializer(vehiculo, data=request.data, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk):
#        vehiculo = get_object_or_404(Vehiculo, pk=pk)
#        vehiculo.delete()
#        return Response({"message": "Vehículo eliminado"}, status=status.HTTP_204_NO_CONTENT)
    
#class MarcaListCreateAPIView(APIView):

#    def get(self, request):
#        marcas = Marca.objects.all()
#        serializer = MarcaSerializer(marcas, many=True)
#        return Response(serializer.data)

#    def post(self, request):
#        serializer = MarcaSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#class PerfilListCreateAPIView(APIView):

#    def get(self, request):
#        perfiles = Perfil.objects.all()
#        serializer = PerfilSerializer(perfiles, many=True)
#        return Response(serializer.data)

#    def post(self, request):
#        serializer = PerfilSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=201)
#        return Response(serializer.errors, status=400)
    
#class PerfilDetailAPIView(APIView):

#    def get(self, request, pk):
#        perfil = get_object_or_404(Perfil, pk=pk)
#        serializer = PerfilSerializer(perfil)
#        return Response(serializer.data)
    
#    def put(self, request, pk):
#        perfil = get_object_or_404(Perfil, pk=pk)
#        serializer = PerfilSerializer(perfil, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def patch(self, request, pk):
#        perfil = get_object_or_404(Perfil, pk=pk)
#        serializer = PerfilSerializer(perfil, data=request.data, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=400)

#    def delete(self, request, pk):
#        perfil = get_object_or_404(Perfil, pk=pk)
#        perfil.delete()
#        return Response({"message": "Perfil eliminado"}, status=status.HTTP_204_NO_CONTENT)
    
#class UserListCreateAPIView(APIView):

#    def get(self, request):
#        users = User.objects.all()
#        serializer = UsuarioSerializer(users, many=True)
#        return Response(serializer.data)

#    def post(self, request):
#        serializer = UsuarioSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=201)
#        return Response(serializer.errors, status=400)

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    @action(detail=True, methods=['post'])
    def comprar(self, request, pk=None):
        vehiculo = self.get_object()

        perfil_id = request.data.get('perfil')
        precio = request.data.get('precio')

        if not perfil_id or not precio:
            return Response(
                {"error": "perfil y precio son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        CompraVehiculo.objects.create(
            vehiculo=vehiculo,
            perfil_id=perfil_id,
            precio=precio,
            fecha_compra=timezone.now()
        )

        return Response(
            {"mensaje": "Compra realizada"},
            status=status.HTTP_201_CREATED
        )
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['marca', 'anho']
    search_fields = ['modelo', 'marca__nombre']
    ordering_fields = ['anho', 'modelo']

class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['finalizado']
    search_fields = ['descripcion']
    ordering_fields = ['coste', 'created_at']
    filterset_fields = {
        'coste': ['gte', 'lte'],
        'duracion': ['gte', 'lte'],
    }

    @action(detail=True, methods=['post'])
    def finalizar (self, request, pk=None):
        mantenimineto = self.get_object()

        if mantenimineto.finalizado:
            return self.response(
                {"error": "El mantenimiento ya está finalizado"},
                status=status.HTTP_409_CONFLICT
            )
        
        mantenimineto.finalizado = True
        mantenimineto.save()

        return Response(
            {"mensaje": "Mantenimiento finalizado correctamente"},
            status=status.HTTP_200_OK
        )

class CompraVehiculoViewSet(viewsets.ModelViewSet):
    queryset = CompraVehiculo.objects.all()
    serializer_class = CompraVehiculoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'precio': ['gte', 'lte']
    }

    ordering_fields = ['precio', 'fecha_compra']

class AccesorioViewSet(viewsets.ModelViewSet):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer