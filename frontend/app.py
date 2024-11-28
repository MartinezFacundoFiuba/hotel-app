from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    print(request.form)
    return render_template('base.html')

@app.route('/hoteles')
def hoteles():
    response = requests.get('http://127.0.0.1:5002/hoteles')
    hotels = response.json()
    return render_template('hoteles.html', hotels=hotels)

@app.route('/hotel_detalle/<int:hotel_id>')
def hotel_detalle(hotel_id):
    response = requests.get(f'http://127.0.0.1:5002/hoteles/{hotel_id}')
    print(response.json())
    hotel = response.json()
    print(hotel)
    return render_template('hotel-detalle.html', hotel=hotel[0])

@app.route('/habitaciones/<int:hotel_id>')
def habitaciones(hotel_id):
    response = requests.get(f'http://127.0.0.1:5002/habitaciones/{hotel_id}')
    rooms = response.json()
    return render_template('rooms-tariff.html', rooms=rooms)

@app.route('/habitacion_detalles/<int:hotel_id>/<int:room_id>')
def habitacion_detalles(hotel_id, room_id):
    response = requests.get(f'http://127.0.0.1:5002/habitaciones/{hotel_id}/{room_id}')
    if response.status_code == 200:
        room = response.json()
    else:
        return "Habitación no encontrada", 404
    return render_template('room-details.html', room=room[0])

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/mensajes', methods=['POST'])
def mensajes():
    return render_template('mensajes.html')

@app.route('/registrar_propietario')
def registro_propietario():
    return render_template('registrar_propietario.html')

@app.route('/registrar_inquilino')
def registro_inquilino():
    return render_template('registrar_inquilino.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/reservas')
def reservas():
    response = requests.get('http://127.0.0.1:5002/hospedaje')
    if response.status_code == 200:
        reservas = response.json()
    else:
        reservas = []
    return render_template('reservas.html', reservas=reservas)

@app.route('/formularioenviado', methods=['POST'])
def formularioenviado():
    print(request.form)
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_inicial = request.form['inicio']
    fecha_final = request.form['final']
    fecha = datetime.now()
    habitacion = request.form['id_habitacion']
    hotel = request.form['id_hotel']
    email = request.form['email']
    usuario = 2 # agregar nombre apellido y mail a las reservas en bbdd, para conseguir el id user con esos datos
    return render_template('formularioenviado.html')

@app.route('/inicio_sesión')
def inicio_sesión():
    return render_template('inicio-de-sesión.html')

@app.route('/inicio_sesión_propietario')
def inicio_sesión_propietario():
    return render_template('inicio-sesión-propietario.html')

@app.route('/inicio_sesión_cliente')
def inicio_sesión_cliente():
    return render_template('inicio-sesión-cliente.html')

@app.route('/reservar/<int:room_id>/<int:hotel_id>')
def reservar(room_id, hotel_id):
    return render_template('reservar.html', room_id=room_id, hotel_id=hotel_id)

@app.route('/cancelar_reserva/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    return "Reserva cancelada", 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)