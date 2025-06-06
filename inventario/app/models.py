from django.db import models
from django.core.exceptions import ValidationError

class Estado(models.Model):
    nombre_est = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.nombre_est

class Municipio(models.Model):
    nombre_mun = models.CharField(max_length=100)
    fk_estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return self.nombre_mun
class RazonSocial(models.Model):
    razon = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    class Meta:
        verbose_name = "Razón Social"
        verbose_name_plural = "Razones Sociales"

    def __str__(self):
        return self.razon
    
class Sucursal(models.Model):
    nombre_suc = models.CharField(max_length=100)
    fk_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    fk_tipo_sucursal = models.ForeignKey('Tipo_Sucursal', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Sucursal")    
    fk_razon_social = models.ForeignKey(RazonSocial, on_delete=models.SET_NULL, null=True, verbose_name="Razón Social")
    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.nombre_suc

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre



class TipoEquipo(models.Model):
    nombre_tipo_equipo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo de Equipo"
        verbose_name_plural = "Tipos de Equipo"

    def __str__(self):
        return self.nombre_tipo_equipo

class TipoAlmacenamiento(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo de Almacenamiento"
        verbose_name_plural = "Tipos de Almacenamiento"

    def __str__(self):
        return self.nombre

class Disponibilidad(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Estado de Disponibilidad"
        verbose_name_plural = "Estados de Disponibilidad"

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=100)
    correo = models.EmailField(null=True, blank=True)
    fk_sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, verbose_name="Sucursal")
    fk_departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, verbose_name="Departamento")
    puesto = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return self.nombre_empleado

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    fecha_de_alta = models.DateField(null=True, blank=True)
    tipo = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50, null=True, blank=True)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    numero_serie = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fk_sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, verbose_name="Sucursal")
    fk_razon_social = models.ForeignKey(RazonSocial, on_delete=models.SET_NULL, null=True, verbose_name="Razón Social")
    tipo_almacenamiento = models.ForeignKey(TipoAlmacenamiento, on_delete=models.SET_NULL, null=True)
    capacidad_almacenamiento = models.IntegerField("Capacidad de almacenamiento (GB)", null=True, blank=True)
    ram = models.IntegerField("Memoria RAM (GB)", null=True, blank=True)
    procesador = models.CharField(max_length=100, null=True, blank=True)
    disponibilidad = models.ForeignKey(Disponibilidad, on_delete=models.SET_NULL, null=True)
    licencia_office = models.BooleanField(default=False, verbose_name="Licencia Office")
    version_windows = models.CharField(max_length=50, null=True, blank=True, verbose_name="Versión de Windows")
    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return f"{self.nombre} - {self.tipo} - {self.marca} {self.modelo}"


class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=100)
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subtipos')

    class Meta:
        verbose_name = "Tipo de Mantenimiento"
        verbose_name_plural = "Tipos de Mantenimiento"

    def __str__(self):
        # Para mostrar el nombre completo en árbol
        nombres = [self.nombre]
        actual = self.padre
        while actual:
            nombres.insert(0, actual.nombre)
            actual = actual.padre
        return ' > '.join(nombres)

    def get_raiz(self):
        actual = self
        while actual.padre:
            actual = actual.padre
        return actual.nombre

class Mantenimiento(models.Model):
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")
    tipo_mantenimiento = models.ForeignKey('TipoMantenimiento', on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Mantenimiento")
    fecha = models.DateField(verbose_name="Fecha")
    diagnostico = models.CharField(max_length=255, verbose_name="Diagnóstico")
    solucion = models.CharField(max_length=255, verbose_name="Solución")
    tecnico = models.CharField(max_length=100, verbose_name="Técnico")
    estatus = models.CharField(max_length=50, default='Pendiente', verbose_name="Estatus")

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"

    def __str__(self):
        return f"Mantenimiento de {self.fk_equipo} ({self.tipo_general})"

    @property
    def tipo_general(self):
        return self.tipo_mantenimiento.get_raiz() if self.tipo_mantenimiento else "N/A"

class Prestamo(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"

    def clean(self):
        if self.fk_equipo.disponibilidad.nombre != 'Disponible':
            raise ValidationError("Este equipo no está disponible para préstamo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        en_prestamo = Disponibilidad.objects.get(nombre='En préstamo')
        self.fk_equipo.disponibilidad = en_prestamo
        self.fk_equipo.save()

    def __str__(self):
        return f"Préstamo de {self.fk_equipo} a {self.fk_empleado}"

class Asignacion(models.Model):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")  
    fecha_asignacion = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Asignacion"
        verbose_name_plural = "Asignaciones"

    def clean(self):
        if self.fk_equipo.disponibilidad.nombre != 'Disponible':
            raise ValidationError("Este equipo no está disponible para asignarse, ya esta asignado alguien mas.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        asignado = Disponibilidad.objects.get(nombre='Asignado')
        self.fk_equipo.disponibilidad = asignado
        self.fk_equipo.save()

    def __str__(self):
        return f"Asignacion de {self.fk_equipo} a {self.fk_empleado}"

class DispositivoMovil(models.Model):
    PLAN_CHOICES = [
        ('Plan', 'Plan'),
        ('Prepago', 'Prepago'),
    ]
    imei = models.CharField(max_length=20)
    modelo = models.CharField(max_length=50)
    numero_celular = models.CharField(max_length=20)
    tipo_plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    fk_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, verbose_name="Equipo")

    class Meta:
        verbose_name = "Dispositivo Móvil"
        verbose_name_plural = "Dispositivos Móviles"

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.numero_celular}"


class Tipo_Sucursal(models.Model):
    nombre_tipo_sucursal = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tipo de Sucursal"
        verbose_name_plural = "Tipos de Sucursal"

    def __str__(self):
        return self.nombre_tipo_sucursal
    
