from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Mantenimiento, Marca, Vehiculo, CompraVehiculo, Accesorio

class UsuarioSerializer(serializers.ModelSerializer):
    perfil = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'perfil']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data.get('email', ''), 
            password=validated_data['password']
        )
        return user

class PerfilSerializer(serializers.ModelSerializer):
    NombreUsuario = serializers.CharField(source='usuario.username', read_only=True)

    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='usuario'
    )

    class Meta:
        model = Perfil
        fields = ['id', 'usuario_id', 'NombreUsuario', 'telefono', 'direccion', 'role']
        read_only_fields = ['role']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class AccesorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accesorio
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    NombreMarca = serializers.CharField(source='marca.nombre', read_only=True)
    perfiles = PerfilSerializer(source='perfil', many=True, read_only=True)
    accesorios = AccesorioSerializer(read_only=True, many=True)

    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(),
        write_only=True,
        source='marca'
    )

    accesorios_id = serializers.PrimaryKeyRelatedField(
        queryset=Accesorio.objects.all(),
        many=True,
        write_only=True,
        source='accesorios',
        required=False
    )

    class Meta:
        model = Vehiculo
        fields = ['id', 'modelo', 'anho', 'marca_id', 'NombreMarca', 'accesorios', 'accesorios_id', 'perfiles']

    def validate_anho(self, value):
        if value < 1886:
            raise serializers.ValidationError("Los coches se crearon casi al final del siglo XIX")
        return value

    def create(self, validated_data):
        accesorios = validated_data.pop('accesorios', [])
        vehiculo = Vehiculo.objects.create(**validated_data)
        if accesorios:
            vehiculo.accesorios.set(accesorios)
        return vehiculo
    
class MantenimientoSerializer(serializers.ModelSerializer):
    DetalleVehiculo = serializers.SerializerMethodField()

    vehiculo_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehiculo.objects.all(),
        write_only=True,
        source='vehiculo'
    )

    class Meta:
        model = Mantenimiento
        fields = [
            'id', 'vehiculo_id', 'DetalleVehiculo',
            'duracion', 'finalizado',
            'descripcion', 'coste',
            'created_at', 'updated_at'
        ]

    def get_DetalleVehiculo(self, obj):
        return f"{obj.vehiculo.marca.nombre} {obj.vehiculo.modelo}"
    
class CompraVehiculoSerializer(serializers.ModelSerializer):
    vehiculo_info = serializers.CharField(source='vehiculo.modelo', read_only=True)
    perfil_info = serializers.CharField(source='perfil.usuario.username', read_only=True)
    
    class Meta:
        model = CompraVehiculo
        fields = ['id', 'vehiculo', 'vehiculo_info',
                  'perfil', 'perfil_info', 'precio', 'fecha_compra']
        read_only_fields = ['fecha_compra']