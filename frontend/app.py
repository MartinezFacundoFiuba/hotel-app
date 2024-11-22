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
@app.route('/registrar_propietario',methods = ["POST","GET"])
def registro_propietario():
    if request.method == 'POST':
        return redirect(url_for('formulario_enviado'))
    else:
        return render_template('registrar_propietario.html')
@app.route('/registro')
def registro():
    return render_template('registro.html')
@app.route('/formulario_enviado')
def formulario_enviado():
    return render_template('formulario_enviado.html')
@app.route("/iniciar_sesion")
def iniciar_sesion():
    return render_template("inicio.html")
if __name__ == '__main__':
    app.run(debug=True, port=5000)