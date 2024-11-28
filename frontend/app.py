from flask import Flask, render_template,session, request, redirect, url_for,session
from flask_login import LoginManager 
import requests
app = Flask(__name__)
app.secret_key = "46934825"
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/hoteles')
def hoteles():
    response = requests.get('http://127.0.0.1:5003/hoteles')
    hotels = response.json()
    print(hotels)
    return render_template('hoteles.html', hotels=hotels)
@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')
@app.route('/habitaciones/<id>')
def habitacion(id):
    response = requests.get(f'http://127.0.0.1:5003/habitaciones/{id}')
    rooms = response.json()
    print(rooms)
    return render_template('rooms-tariff.html', rooms=rooms)
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
@app.route('/reservar/')
def reservar():
    response = requests.get(f'http://127.0.0.1:5003/hospedaje')
    rooms = response.json()
   
    return render_template('room-details.html',rooms= rooms)

@app.route('/formulario_enviado')
def formulario_enviado():
    print(session)
    return render_template('formulario_enviado.html')
@app.route("/iniciar_sesion",methods = ["POST","GET"])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")
        url = "http://127.0.0.1:5003/iniciar_sesion"
        datos={"email":email,"contraseña":contraseña
        }
        response = requests.post(url, json=datos)
        print(response)
        if response.status_code == 200:
            datos = response.json()
            print(datos[1]['email'])
            session['email'] = datos[1]['email'] 
        return redirect(url_for('formulario_enviado'))
    else:

        return render_template('inicio.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)