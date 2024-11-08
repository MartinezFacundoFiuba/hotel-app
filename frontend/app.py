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

@app.route('/hotels')
def hotels():
    # Simulación de datos de hoteles (esto podría venir de una base de datos)
    hotels = [
        {'id': 1, 'name': 'Hotel Lux', 'location': 'Ciudad A'},
        {'id': 2, 'name': 'Hotel Comfort', 'location': 'Ciudad B'},
        # Agrega más hoteles según sea necesario
    ]
    return render_template('hotels.html', hotels=hotels)  # Renderiza la plantilla de hoteles

@app.route('/room-details/<int:room_id>')
def room_details(room_id):
    # Simulación de datos de habitaciones (esto podría venir de una base de datos)
    rooms = {
        1: {
            'title': 'Luxurious Suites',
            'images': ['8.jpg', '9.jpg', '10.jpg'],
            'description': 'Descripción de la suite lujosa...',
            'size': '44 sq',
            'price': '$200.00',
            'amenities': [
                'Una de las mayores barreras para hacer la venta es su perspectiva.',
                'Principio para trabajar y ganar más dinero mientras se divierte más.',
                'Personas desafortunadas. No se obstine.',
                'Espacio en su casa Cómo vender más rápido que sus vecinos.'
            ]
        },
        # Agrega más habitaciones según sea necesario
    }

    room = rooms.get(room_id)
    if room is None:
        return "Room not found", 404

    return render_template('room-details.html', room=room)

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