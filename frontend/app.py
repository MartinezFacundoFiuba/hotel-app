from flask import Flask, render_template,session, request, redirect, url_for,session
from flask_login import LoginManager 
import requests
from datetime import datetime, timedelta
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
   
    # Obtener el mes y año actuales
    hoy = datetime.today()
    mes = hoy.month
    año = hoy.year

    # Obtener el primer día del mes y el número de días en el mes
    primer_dia = datetime(año, mes, 1)
    ultimo_dia = datetime(año, mes + 1, 1) - timedelta(days=1)
    dias_en_mes = (ultimo_dia - primer_dia).days + 1

    # Crear una lista de días del mes para renderizar en el calendario
    calendario = []
    for dia in range(1, dias_en_mes + 1):
        fecha = datetime(año, mes, dia).date()  # Fecha del día actual
        calendario.append({
            'fecha': fecha,
            'disponible': fecha in rooms  # Verificar si la fecha está en el set de fechas disponibles
        })
    print(calendario)
    unavailable_days = [ {'date': '2024-11-25'}, {'date': '2024-11-14'}, {'date': '2025-01-01'} ]
    return render_template('room-details.html', unavailable_days=unavailable_days)

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