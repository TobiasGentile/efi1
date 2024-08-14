from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/efi_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configura la clave secreta
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mi_clave_secreta_por_defecto')

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos y rutas después de inicializar la app
    with app.app_context():
        from models import Equipo, Modelo, Categoria, Marca, Fabricante, Caracteristica, Stock, Accesorio, Proveedor
        from forms import EquipoForm
        
        # Registrar las rutas
        @app.route('/')
        def inicio():
            return render_template('index.html')

        @app.route('/equipos', methods=['GET'])
        def listar_equipos():
            equipos = Equipo.query.all()
            return render_template('listar_equipos.html', equipos=equipos)

        @app.route('/equipo/nuevo', methods=['GET', 'POST'])
        def nuevo_equipo():
            form = EquipoForm()
            form.populate_choices()
            if form.validate_on_submit():
                nuevo_equipo = Equipo(
                    nombre=form.nombre.data,
                    modelo_id=form.modelo_id.data,
                    categoria_id=form.categoria_id.data,
                    costo=form.costo.data
                )
                db.session.add(nuevo_equipo)
                db.session.commit()
                return redirect(url_for('listar_equipos'))
            return render_template('equipo_form.html', form=form, form_title="Añadir Nuevo Equipo")

        @app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
        def equipo_edit(id):
            equipo = Equipo.query.get_or_404(id)
            form = EquipoForm(obj=equipo)
            form.populate_choices()
            if form.validate_on_submit():
                equipo.nombre = form.nombre.data
                equipo.modelo_id = form.modelo_id.data
                equipo.categoria_id = form.categoria_id.data
                equipo.costo = form.costo.data
                db.session.commit()
                return redirect(url_for('listar_equipos'))
            return render_template('equipo_form.html', form=form, form_title="Editar Equipo")

    @app.route('/modelos')
    def modelos():
        modelos = Modelo.query.all()
        return render_template('modelos.html', modelos=modelos)

    @app.route('/modelo/nuevo', methods=['GET', 'POST'])
    def nuevo_modelo():
        form = nuevo_modelo()
        if form.validate_on_submit():
            modelo = Modelo(nombre=form.nombre.data, marca_id=form.marca_id.data, fabricante_id=form.fabricante_id.data)
            db.session.add(modelo)
            db.session.commit()
            return redirect(url_for('modelos'))
        return render_template('nuevo_modelo.html', form=form)

    @app.route('/modelo/<int:id>')
    def ver_modelo(id):
        modelo = Modelo.query.get_or_404(id)
        return render_template('ver_modelo.html', modelo=modelo)

    @app.route('/modelo/<int:id>/editar', methods=['GET', 'POST'])
    def editar_modelo(id):
        modelo = Modelo.query.get_or_404(id)
        form = nuevo_modelo(obj=modelo)
        if form.validate_on_submit():
            form.populate_obj(modelo)
            db.session.commit()
            return redirect(url_for('modelos'))
        return render_template('editar_modelo.html', form=form)

    @app.route('/modelo/<int:id>/eliminar', methods=['POST'])
    def eliminar_modelo(id):
        modelo = Modelo.query.get_or_404(id)
        db.session.delete(modelo)
        db.session.commit()
        return redirect(url_for('modelos'))

    @app.route('/categorias')
    def categorias():
        categorias = Categoria.query.all()
        return render_template('categorias.html', categorias=categorias)

    @app.route('/categoria/nueva', methods=['GET', 'POST'])
    def nueva_categoria():
        form = nueva_categoria()
        if form.validate_on_submit():
            categoria = Categoria(nombre=form.nombre.data)
            db.session.add(categoria)
            db.session.commit()
            return redirect(url_for('categorias'))
        return render_template('nueva_categoria.html', form=form)

    @app.route('/categoria/<int:id>')
    def ver_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        return render_template('ver_categoria.html', categoria=categoria)

    @app.route('/categoria/<int:id>/editar', methods=['GET', 'POST'])
    def editar_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        form = nueva_categoria(obj=categoria)
        if form.validate_on_submit():
            form.populate_obj(categoria)
            db.session.commit()
            return redirect(url_for('categorias'))
        return render_template('editar_categoria.html', form=form)

    @app.route('/categoria/<int:id>/eliminar', methods=['POST'])
    def eliminar_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        db.session.delete(categoria)
        db.session.commit()
        return redirect(url_for('categorias'))

    @app.route('/marcas')
    def marcas():
        marcas = Marca.query.all()
        return render_template('marcas.html', marcas=marcas)

    @app.route('/marca/nueva', methods=['GET', 'POST'])
    def nueva_marca():
        form = nueva_marca()
        if form.validate_on_submit():
            marca = Marca(nombre=form.nombre.data)
            db.session.add(marca)
            db.session.commit()
            return redirect(url_for('marcas'))
        return render_template('nueva_marca.html', form=form)

    @app.route('/marca/<int:id>')
    def ver_marca(id):
        marca = Marca.query.get_or_404(id)
        return render_template('ver_marca.html', marca=marca)

    @app.route('/marca/<int:id>/editar', methods=['GET', 'POST'])
    def editar_marca(id):
        marca = Marca.query.get_or_404(id)
        form = nueva_marca(obj=marca)
        if form.validate_on_submit():
            form.populate_obj(marca)
            db.session.commit()
            return redirect(url_for('marcas'))
        return render_template('editar_marca.html', form=form)

    @app.route('/marca/<int:id>/eliminar', methods=['POST'])
    def eliminar_marca(id):
        marca = Marca.query.get_or_404(id)
        db.session.delete(marca)
        db.session.commit()
        return redirect(url_for('marcas'))

    @app.route('/fabricantes')
    def fabricantes():
        fabricantes = Fabricante.query.all()
        return render_template('fabricantes.html', fabricantes=fabricantes)

    @app.route('/fabricante/nuevo', methods=['GET', 'POST'])
    def nuevo_fabricante():
        form = nuevo_fabricante()
        if form.validate_on_submit():
            fabricante = Fabricante(nombre=form.nombre.data)
            db.session.add(fabricante)
            db.session.commit()
            return redirect(url_for('fabricantes'))
        return render_template('nuevo_fabricante.html', form=form)

    @app.route('/fabricante/<int:id>')
    def ver_fabricante(id):
        fabricante = Fabricante.query.get_or_404(id)
        return render_template('ver_fabricante.html', fabricante=fabricante)

    @app.route('/fabricante/<int:id>/editar', methods=['GET', 'POST'])
    def editar_fabricante(id):
        fabricante = Fabricante.query.get_or_404(id)
        form = nuevo_fabricante(obj=fabricante)
        if form.validate_on_submit():
            form.populate_obj(fabricante)
            db.session.commit()
            return redirect(url_for('fabricantes'))
        return render_template('editar_fabricante.html', form=form)

    @app.route('/fabricante/<int:id>/eliminar', methods=['POST'])
    def eliminar_fabricante(id):
        fabricante = Fabricante.query.get_or_404(id)
        db.session.delete(fabricante)
        db.session.commit()
        return redirect(url_for('fabricantes'))

    @app.route('/caracteristicas')
    def caracteristicas():
        caracteristicas = Caracteristica.query.all()
        return render_template('caracteristicas.html', caracteristicas=caracteristicas)

    @app.route('/caracteristica/nueva', methods=['GET', 'POST'])
    def nueva_caracteristica():
        form = nueva_caracteristica()
        if form.validate_on_submit():
            caracteristica = Caracteristica(nombre=form.nombre.data)
            db.session.add(caracteristica)
            db.session.commit()
            return redirect(url_for('caracteristicas'))
        return render_template('nueva_caracteristica.html', form=form)

    @app.route('/caracteristica/<int:id>')
    def ver_caracteristica(id):
        caracteristica = Caracteristica.query.get_or_404(id)
        return render_template('ver_caracteristica.html', caracteristica=caracteristica)

    @app.route('/caracteristica/<int:id>/editar', methods=['GET', 'POST'])
    def editar_caracteristica(id):
        caracteristica = Caracteristica.query.get_or_404(id)
        form = nueva_caracteristica(obj=caracteristica)
        if form.validate_on_submit():
            form.populate_obj(caracteristica)
            db.session.commit()
            return redirect(url_for('caracteristicas'))
        return render_template('editar_caracteristica.html', form=form)

    @app.route('/caracteristica/<int:id>/eliminar', methods=['POST'])
    def eliminar_caracteristica(id):
        caracteristica = Caracteristica.query.get_or_404(id)
        db.session.delete(caracteristica)
        db.session.commit()
        return redirect(url_for('caracteristicas'))

    @app.route('/stocks')
    def stocks():
        stocks = Stock.query.all()
        return render_template('stocks.html', stocks=stocks)

    @app.route('/stock/nuevo', methods=['GET', 'POST'])
    def nuevo_stock():
        form = nuevo_stock()
        if form.validate_on_submit():
            stock = Stock(cantidad=form.cantidad.data, modelo_id=form.modelo_id.data)
            db.session.add(stock)
            db.session.commit()
            return redirect(url_for('stocks'))
        return render_template('nuevo_stock.html', form=form)

    @app.route('/stock/<int:id>')
    def ver_stock(id):
        stock = Stock.query.get_or_404(id)
        return render_template('ver_stock.html', stock=stock)

    @app.route('/stock/<int:id>/editar', methods=['GET', 'POST'])
    def editar_stock(id):
        stock = Stock.query.get_or_404(id)
        form = nuevo_stock(obj=stock)
        if form.validate_on_submit():
            form.populate_obj(stock)
            db.session.commit()
            return redirect(url_for('stocks'))
        return render_template('editar_stock.html', form=form)

    @app.route('/stock/<int:id>/eliminar', methods=['POST'])
    def eliminar_stock(id):
        stock = Stock.query.get_or_404(id)
        db.session.delete(stock)
        db.session.commit()
        return redirect(url_for('stocks'))
    
    @app.route('/stock/<int:id>/eliminar', methods=['POST'])
    def eliminar_stock(id):
        stock = Stock.query.get_or_404(id)
        db.session.delete(stock)
        db.session.commit()
        return redirect(url_for('stocks'))

    @app.route('/accesorio/nuevo', methods=['GET', 'POST'])
    def nuevo_accesorio():
        form = nuevo_accesorio()
        if form.validate_on_submit():
            accesorio = Accesorio(tipo=form.tipo.data, descripcion=form.descripcion.data, equipo_id=form.equipo_id.data)
            db.session.add(accesorio)
            db.session.commit()
            return redirect(url_for('accesorios'))
        return render_template('nuevo_accesorio.html', form=form)

    @app.route('/accesorio/<int:id>')
    def ver_accesorio(id):
        accesorio = Accesorio.query.get_or_404(id)
        return render_template('ver_accesorio.html', accesorio=accesorio)

    @app.route('/accesorio/<int:id>/editar', methods=['GET', 'POST'])
    def editar_accesorio(id):
        accesorio = Accesorio.query.get_or_404(id)
        form = nuevo_accesorio(obj=accesorio)
        if form.validate_on_submit():
            form.populate_obj(accesorio)
            db.session.commit()
            return redirect(url_for('accesorios'))
        return render_template('editar_accesorio.html', form=form)

    @app.route('/accesorio/<int:id>/eliminar', methods=['POST'])
    def eliminar_accesorio(id):
        accesorio = Accesorio.query.get_or_404(id)
        db.session.delete(accesorio)
        db.session.commit()
        return redirect(url_for('accesorios'))
    
    @app.route('/proveedores')
    def proveedores():
        proveedores = Proveedor.query.all()
        return render_template('proveedores.html', proveedores=proveedores)

    @app.route('/proveedor/nuevo', methods=['GET', 'POST'])
    def nuevo_proveedor():
        form = nuevo_proveedor()
        if form.validate_on_submit():
            proveedor = Proveedor(nombre=form.nombre.data, contacto=form.contacto.data)
            db.session.add(proveedor)
            db.session.commit()
            return redirect(url_for('proveedores'))
        return render_template('nuevo_proveedor.html', form=form)

    @app.route('/proveedor/<int:id>')
    def ver_proveedor(id):
        proveedor = Proveedor.query.get_or_404(id)
        return render_template('ver_proveedor.html', proveedor=proveedor)

    @app.route('/proveedor/<int:id>/editar', methods=['GET', 'POST'])
    def editar_proveedor(id):
        proveedor = Proveedor.query.get_or_404(id)
        form = nuevo_proveedor(obj=proveedor)
        if form.validate_on_submit():
            form.populate_obj(proveedor)
            db.session.commit()
            return redirect(url_for('proveedores'))
        return render_template('editar_proveedor.html', form=form)

    @app.route('/proveedor/<int:id>/eliminar', methods=['POST'])
    def eliminar_proveedor(id):
        proveedor = Proveedor.query.get_or_404(id)
        db.session.delete(proveedor)
        db.session.commit()
        return redirect(url_for('proveedores'))



    return app
