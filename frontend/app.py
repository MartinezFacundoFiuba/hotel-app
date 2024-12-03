from flask import Flask, render_template, request, redirect, url_for, session, abort
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '1234567890'
app.permanent_session_lifetime = timedelta(days=30)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session.permanent = True
        user = {}
        email = request.form['email']
        try:
            response = requests.get(f'http://127.0.0.1:5002/usuario/{email}')
            user = response.json()
            print(user)
            session['user'] = user
            return render_template('base.html', user=session.get('user'))
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return render_template('base.html')
    elif 'user' in session:
        return render_template('base.html', user=session.get('user'))
    else:
        return render_template('base.html')

@app.route('/hoteles')
def hoteles():
    try:
        response = requests.get('http://127.0.0.1:5002/hoteles')
        hotels = response.json()
    except Exception as e:
        print(f"Error al obtener hoteles: {e}")
        hotels = []
    if 'user' in session:
        user = session.get('user')
        if user[0]['rol'] == 'propietario':
            hotels = [hotel for hotel in hotels if hotel['propietario_id'] == user[0]['id']]
        return render_template('hoteles.html', hotels=hotels, user=user)
    else:
        return render_template('hoteles.html', hotels=hotels)

@app.route('/hotel_detalle/<int:hotel_id>')
def hotel_detalle(hotel_id):
    try:
        response = requests.get(f'http://127.0.0.1:5002/hoteles/{hotel_id}')
        hotel = response.json()
        print(hotel, "Hotel")
    except Exception as e:
        print(f"Error al obtener detalles del hotel: {e}")
        return "Error al obtener detalles del hotel", 500
    if 'user' in session:
        user = session.get('user')
        return render_template('hotel-detalle.html', hotel=hotel[0], user=user)
    else:
        return render_template('hotel-detalle.html', hotel=hotel[0])

@app.route('/habitaciones/<int:hotel_id>')
def habitaciones(hotel_id):
    try:
        response = requests.get(f'http://127.0.0.1:5002/habitaciones/{hotel_id}')
        rooms = response.json()
    except Exception as e:
        print(f"Error al obtener habitaciones: {e}")
        rooms = []
    if 'user' in session:
        user = session.get('user')
        return render_template('rooms-tariff.html', rooms=rooms, user=user)
    else:
        return render_template('rooms-tariff.html', rooms=rooms)

@app.route('/habitacion_detalles/<int:hotel_id>/<int:room_id>')
def habitacion_detalles(hotel_id, room_id):
    try:
        response = requests.get(f'http://127.0.0.1:5002/habitaciones/{hotel_id}/{room_id}')
        if response.status_code == 200:
            room = response.json()
        else:
            return "Habitación no encontrada", 404
    except Exception as e:
        print(f"Error al obtener detalles de la habitación: {e}")
        return "Error al obtener detalles de la habitación", 500
    if 'user' in session:
        user = session.get('user')
        return render_template('room-details.html', room=room[0], user=user)
    else:
        return render_template('room-details.html', room=room[0])

@app.route('/contacto')
def contacto():
    if 'user' not in session:
        return redirect(url_for('inicio_sesion'))
    else:
        return render_template('contacto.html', user=session.get('user'))

@app.route('/mensajes', methods=['POST'])
def mensajes():
    if 'user' not in session:
        return redirect(url_for('inicio_sesion'))
    else:
        return render_template('mensajes.html', user=session.get('user'))

@app.route('/registrar_propietario')
def registro_propietario():
    return render_template('registrar_propietario.html', user=session.get('user'))

@app.route('/registrar_inquilino')
def registro_inquilino():
    return render_template('registrar_inquilino.html', user=session.get('user'))

@app.route('/registro')
def registro():
    if 'user' in session:
        return redirect(url_for('home'))
    else:
        return render_template('registro.html')

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if 'user' not in session:
        return redirect(url_for('inicio_sesion'))
    user = session.get('user')
    reservas = []
    if request.method == 'POST':
        reserva_id = request.form.get('reserva_id')
        try:
            requests.delete(f'http://127.0.0.1:5002/hospedaje/{reserva_id}')
        except Exception as e:
            print(f"Error al cancelar reserva: {e}")
        try:
            response = requests.get(f'http://127.0.0.1:5002/hospedaje/{user[0]["email"]}')
            if response.status_code == 200:
                reservas = response.json()
        except Exception as e:
            print(f"Error al obtener reservas: {e}")
        return redirect(url_for('reservas', reservas=reservas))
    try:
        response = requests.get(f'http://127.0.0.1:5002/hospedaje/{user[0]["email"]}')
        if response.status_code == 200:
            reservas = response.json()
    except Exception as e:
        print(f"Error al obtener reservas: {e}")
    return render_template('reservas.html', reservas=reservas, user=user)

@app.route('/formularioenviado', methods=['POST'])
def formularioenviado():
    if 'user' not in session:
        return redirect(url_for('inicio_sesion'))
    user = session.get('user')
    solicitud = {
        "hotel_id": int(request.form['hotel_id']),
        "usuario_id": user[0]['id'],
        "fecha_inicial": request.form['inicio_reserva'],
        "fecha_final": request.form['final_reserva'],
        "habitacion_id": int(request.form['habitacion_id']),
        "email": user[0]['email']
    }
    print(solicitud)
    try:
        requests.post('http://127.0.0.1:5002/hospedaje', json=solicitud)
    except Exception as e:
        print(f"Error al enviar datos a hospedaje: {e}")
    return render_template('formularioenviado.html', user=user)

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST' and 'empresa' in request.form and request.form['empresa']:
        print(request.form)
        try:
            requests.post('http://127.0.0.1:5002/propietario', json=request.form)
        except Exception as e:
            print(f"Error al enviar datos a propietario: {e}")
    elif request.method == 'POST':
        print(request.form, "Form de usuario")
        try:
            requests.post('http://127.0.0.1:5002/usuario', json=request.form)
        except Exception as e:
            print(f"Error al enviar datos a usuario: {e}")
    elif 'user' in session:
        return redirect(url_for('home'))
    return render_template('inicio-de-sesion.html')

@app.route('/reservar/<int:room_id>/<int:hotel_id>')
def reservar(room_id, hotel_id):
    if 'user' not in session:
        return redirect(url_for('inicio_sesion'))
    user = session.get('user')
    reservas = []
    fechas_reservadas = []
    try:
        response = requests.get(f'http://127.0.0.1:5002/hospedaje/{hotel_id}/{room_id}')
        print(response, "Response")
        if response.status_code == 200:
            reservas = response.json()
            next = timedelta(days=1)
            for reserva in reservas:
                print(reserva, "Reserva")
                inicio = datetime.strptime(reserva["fecha_inicial"], "%Y-%m-%d")
                fin = datetime.strptime(reserva["fecha_final"], "%Y-%m-%d")
                current = inicio
                while current <= fin:
                    fechas_reservadas.append(current.strftime("%Y-%m-%d"))
                    current += next
                
    except Exception as e:
        print(f"Error al obtener reservas: {e}")
    print(fechas_reservadas, "Fechas reservadas")
    return render_template('reservar.html', room_id=room_id, hotel_id=hotel_id, user=user, fechas_reservadas=fechas_reservadas)

@app.route('/crear_hotel')
def crear_hotel():
    if 'user' not in session:
        return redirect(url_for('inicio_sesion'))
    user = session.get('user')
    return render_template('crear_hotel.html', user=user)

@app.route('/hotelenviado', methods=['POST'])
def hotelenviado():
    print(request.form)
    user = session.get('user')
    print(user)
    solicitud = {
        "nombre": request.form['nombre'],
        "provincia": request.form['provincia'],
        "ciudad": request.form['ciudad'],
        "latitud": request.form['latitud'],
        "longitud": request.form['longitud'],
        "propietario_id": user[0]['id']
    }
    try:
        requests.post('http://127.0.0.1:5002/hoteles', json=solicitud)
    except Exception as e:
        print(f"Error al enviar datos a hotel: {e}")
    return render_template('hotel_creado.html', user=user)

@app.route('/editar_hotel/<int:hotel_id>')
def editar_hotel(hotel_id):
    user = session.get('user')
    habitaciones = []
    try:
        response = requests.get(f'http://127.0.0.1:5002/habitaciones/{hotel_id}')
        habitaciones = response.json()
    except Exception as e:
        print(f"Error al obtener habitaciones: {e}")
    return render_template('editar_hotel.html', hotel_id=hotel_id, user=user, habitaciones=habitaciones)

@app.route('/agregar_habitacion', methods=['POST'])
def agregar_habitacion():
    print(request.form)
    solicitud = {
        "hotel_id": request.form['hotel_id'],
        "habitacion": request.form['numero_habitacion'],
        "piso": request.form['piso'],
        "precio": request.form['precio']
    }
    try:
        requests.post('http://127.0.0.1:5002/habitacion', json=solicitud)
    except Exception as e:
        print(f"Error al enviar datos a habitaciones: {e}")
    return redirect(url_for('editar_hotel', hotel_id=request.form['hotel_id']))

@app.route('/eliminar_habitacion/<int:habitacion_id>/<int:hotel_id>', methods=['POST'])
def eliminar_habitacion(habitacion_id, hotel_id):
    print(habitacion_id, hotel_id)
    try:
        requests.delete(f'http://127.0.0.1:5002/habitacion/{habitacion_id}')
    except Exception as e:
        print(f"Error al eliminar habitación: {e}")
    return redirect(url_for('editar_hotel', hotel_id=hotel_id))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)