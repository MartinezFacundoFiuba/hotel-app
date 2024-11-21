from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')
@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')
@app.route('/ubicaciones')
def ubicaciones():
    return render_template('ubicaciones.html')
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
@app.route('/registrar_propietario')
def registro_propietario():
    return render_template('registrar_propietario.html')
@app.route('/registrar_inquilino')
def registro_inquilino():
    return render_template('registrar_inquilino.html')
@app.route('/registro')
def registro():
    return render_template('registro.html')
@app.route('/registrados')
def registrados():
    return render_template('registrados.html')
@app.route('/inicio_sesión')
def inicio_sesión():
    return render_template('inicio-de-sesión.html')
@app.route('/inicio_sesión_propietario')
def inicio_sesión_propietario():
    return render_template('inicio-sesión-propietario.html')
@app.route('/inicio_sesión_cliente')
def inicio_sesión_cliente():
    return render_template('inicio-sesión-cliente.html')
if __name__ == '__main__':
    app.run(debug=True, port=8000)