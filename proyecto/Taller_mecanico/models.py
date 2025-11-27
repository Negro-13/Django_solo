from django.db import models

class Persona(models.Model):
    dni = models.CharField(max_length=20, primary_key=True)
    apellido = models.CharField(max_length=40)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    tele_contac = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cliente(models.Model):
    cod_cliente = models.CharField(max_length=20, primary_key=True)
    dni = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column='dni')

    def __str__(self):
        return self.cod_cliente

class TipoVehiculo(models.Model):
    cod_tipo_vehiculo = models.CharField(max_length=5, primary_key=True)
    descripcion = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.descripcion

class Marca(models.Model):
    cod_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class FichaTecnica(models.Model):
    nro_ficha = models.AutoField(primary_key=True)
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cod_cliente', blank=True, null=True)
    vehiculo = models.CharField(max_length=12)
    fecha_ingreso = models.DateField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mano_obra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_general = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    servicios = models.ManyToManyField(Servicio, through='DetalleFichaServicio')

    def __str__(self):
        return f"Ficha {self.nro_ficha} - {self.vehiculo}"

class DetalleFichaServicio(models.Model):
    ficha = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ficha} - {self.servicio}"

class Presupuesto(models.Model):
    nro_presupuesto = models.AutoField(primary_key=True)
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cod_cliente', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    total_presupuesto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_gastado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    servicios = models.ManyToManyField(Servicio, through='DetallePresupuestoServicio')

    def __str__(self):
        return f"Presupuesto {self.nro_presupuesto} - {self.cod_cliente}"

class DetallePresupuestoServicio(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.presupuesto} - {self.servicio}"

class Proveedor(models.Model):
    cod_proveedor = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    cod_repuesto = models.CharField(max_length=30, primary_key=True)
    descripcion = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.descripcion
