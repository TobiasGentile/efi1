from app import db  # Asegúrate de importar db correctamente

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais_origen = db.Column(db.String(100), nullable=False)
    modelos = db.relationship('Modelo', backref='fabricante', lazy=True)

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    modelos = db.relationship('Modelo', backref='marca', lazy=True)  # Establece la relación con Modelo

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    equipos = db.relationship('Equipo', backref='modelo', lazy=True)
    accesorios = db.relationship('Accesorio', backref='modelo', lazy=True)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    equipos = db.relationship('Equipo', backref='categoria', lazy=True)

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    stock = db.relationship('Stock', uselist=False, backref='equipo', lazy=True)
    caracteristicas = db.relationship('Caracteristica', backref='equipo', lazy=True)
    accesorios = db.relationship('AccesorioEquipo', backref='equipo', lazy=True)  # Nueva relación para accesorios del equipo

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    equipos = db.relationship('Equipo', backref='proveedor', lazy=True)
    accesorios = db.relationship('Accesorio', backref='proveedor', lazy=True)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    ubicacion_almacen = db.Column(db.String(100), nullable=False)

class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)

class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    equipos = db.relationship('AccesorioEquipo', backref='accesorio', lazy=True)  # Nueva relación para equipos que usan este accesorio

# Tabla intermedia para relacionar Equipos y Accesorios
class AccesorioEquipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorio.id'), nullable=False)
