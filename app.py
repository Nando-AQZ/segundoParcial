from flask import Flask,request,render_template,url_for,redirect,session

app = Flask(__name__)
app.secret_key='CLAVE SEGURA'


@app.route("/")
def index():
    if 'lista' not in session:
        # Inicializar carrito como lista
        session['lista'] = []
           
    return render_template('index.html',lista = session['lista'])
   
@app.route("/procesa", methods=['POST'])
def procesa():
    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    fecha = request.form.get('fecha')
    categoria = request.form.get('categoria')

    # Inicializar lista y contador de IDs si no existen
    if 'lista' not in session:
        session['lista'] = []
    
    # Inicializar 'next_id' si no existe
    if 'next_id' not in session:
        session['next_id'] = 1  # Inicializar el contador de IDs

    # Obtener el siguiente ID y actualizar el contador
    id = session['next_id']
    session['next_id'] += 1

    # Agregar el producto a la lista
    session['lista'].append({
        'id': id,
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio,
        'fecha': fecha,
        'categoria': categoria
    })
    session.modified = True

    return redirect(url_for("index"))

@app.route("/eliminar/<int:item_index>", methods=['POST'])
def eliminar(item_index):
    if 'lista' in session and 0 <= item_index < len(session['lista']):
        del session['lista'][item_index]
        session.modified = True
    return redirect(url_for("index"))

@app.route("/modificar/<int:item_index>", methods=['GET', 'POST'])
def modificar(item_index):
    if request.method == 'POST':
        # Obtener los datos del formulario
        id = request.form.get('id')
        nombre = request.form.get('nombre')
        cantidad = int(request.form.get('cantidad'))
        precio = float(request.form.get('precio'))   
        fecha = request.form.get('fecha')
        categoria = request.form.get('categoria') # Obtiene la lista de seminarios seleccionados

        # Verifica si 'lista' existe en la sesión
        if 'lista' not in session:
            session['lista'] = []

        # Modifica solo los campos especificados
        if id:
            session['lista'][item_index]['id'] = id
        if nombre:
            session['lista'][item_index]['nombre'] = nombre
        if cantidad:
            session['lista'][item_index]['cantidad'] = cantidad
        if precio:
            session['lista'][item_index]['precio'] = precio
        if fecha:
            session['lista'][item_index]['fecha'] = fecha 
        if categoria:
            session['lista'][item_index]['categoria'] = categoria  # Concatena la lista en una cadena

        session.modified = True
        
        return redirect(url_for("index"))  # Redirige a la página principal después de la modificación

    # Si es un GET, muestra el formulario con los datos actuales
    item = session['lista'][item_index]
    return render_template('modificar.html', item=item, item_index=item_index)


@app.route('/add_producto')
def add_producto():
    return render_template('add_producto.html')

if __name__=="__main__":
    app.run(debug=True)
