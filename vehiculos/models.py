from django.db import models
from django.contrib.auth.models import User
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=9)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
class Accesorio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre
    
class Vehiculo(models.Model):
    modelo = models.CharField(max_length=100)
    anho = models.IntegerField()
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='vehiculos')
    perfil = models.ManyToManyField('Perfil', through='CompraVehiculo' )
    accesorios = models.ManyToManyField(Accesorio, related_name='vehiculos', blank=True)

    class Meta:
        ordering = ['modelo']
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"

    def __str__(self):
        return f"{self.marca.nombre} | {self.modelo}"

class Mantenimiento(models.Model):
    duracion = models.DurationField()
    descripcion = models.TextField()
    coste = models.DecimalField(max_digits=10, decimal_places=2)
    finalizado = models.BooleanField(default=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='mantenimientos')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"

    def __str__(self):
        return f"Mantenimiento de {self.vehiculo.modelo} comprado por {self.perfil.usuario.username} - {self.precio}€"

class CompraVehiculo(models.Model):
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField()

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        constraints = [
            models.UniqueConstraint(
                fields=['vehiculo', 'perfil'], 
                name='unique_compra'
            )
        ]

    def __str__(self):
        return f"{self.vehiculo.modelo} comprado por {self.precio}"