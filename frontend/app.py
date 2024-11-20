from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Aquí puedes manejar la lógica de suscripción, como guardar el correo en una base de datos
    email = request.form.get('email')
    # Lógica para procesar la suscripción
    print(f'Subscribed email: {email}')  # Solo un ejemplo, reemplaza con tu lógica
    return redirect(url_for('home'))  # Redirige a la página principal después de suscribirse

@app.route('/rooms-tariff')
def rooms_tariff():
    return render_template('rooms-tariff.html')


@app.route('/reserva/<int:room_id>', methods=['POST'])
def reserve(room_id):
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    guests = request.form['guests']
    # Aquí procesarías los datos de la reserva
    return f"Reserva hecha para la Habitación: {room_id} desde {checkin} al {checkout} para {guests} invitado(s)."



@app.route('/hotels')
def hotels():
    # Simulación de datos de hoteles (esto podría venir de una base de datos)
    hotels = [
        {'id': 1, 'name': 'Hotel Lux', 'location': 'Ciudad A'},
        {'id': 2, 'name': 'Hotel Comfort', 'location': 'Ciudad B'},
        # Agrega más hoteles según sea necesario
    ]
    return render_template('hotels.html', hotels=hotels)  # Renderiza la plantilla de hoteles

@app.route('/room-details')
def room_details():
    rooms = [
        {
            'id': 1,
            'title': 'Opción Single',
            'images': ['1.jpg', '2.jpg'],
            'description': 'Una habitación lujosa con vista al mar. Para uno.',
            'amenities': ['WiFi', 'TV', 'Aire acondicionado'],
            'size': '35 m²',
            'price': '$150usd Por Noche'
        },
        {
            'id': 2,
            'title': 'Opción Doble',
            'images': ['3.jpg', '4.jpg'],
            'description': 'Perfecta para parejas, con mucho espacio.',
            'amenities': ['WiFi', 'TV', 'Balcón'],
            'size': '50 m²',
            'price': '$200usd Por Noche'
        },
        {
            'id': 3,
            'title': 'Opción Triple',
            'images': ['5.jpg', '6.jpg'],
            'description': 'Ideal para un viaje de amigos.',
            'amenities': ['WiFi', 'Escritorio', 'TV'],
            'size': '70 m²',
            'price': '$400usd Por Noche'
        },
        {
            'id': 4,
            'title': 'Opción Familiar',
            'images': ['7.jpg', '8.jpg'],
            'description': 'Experiencia de lujo para toda la familia.',
            'amenities': ['WiFi', 'Jacuzzi', 'Servicio de habitaciones'],
            'size': '120 m²',
            'price': '$1000'
        }
    ]
    return render_template('room-details.html', rooms=rooms)


@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
