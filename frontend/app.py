from flask import Flask, render_template,session, request, redirect, url_for,session
from flask_login import LoginManager 
import requests
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = "1"
@app.route('/')
def home():
    response = requests.get('http://127.0.0.1:5003/ofertas')
    ofertas = response.json()

    return render_template('index.html',ofertas=ofertas)
@app.route('/hoteles')
def hoteles():
    response = requests.get('http://127.0.0.1:5003/hoteles')
    hotels = response.json()
    return render_template('hoteles.html', hotels=hotels)
@app.route('/habitaciones')
def habitaciones():
    
    return render_template('habitaciones.html')
@app.route('/habitaciones/<id>')
def habitacion(id):
    response = requests.get(f'http://127.0.0.1:5003/habitaciones/{id}')
    rooms = response.json()
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
@app.route('/hoteles/<hotel>/<habitacion>/reserva',methods = ["POST","GET"])
def reserva(hotel,habitacion):
    if request.method == 'POST':
        nhj=1
    else:
        response = requests.get(f'http://127.0.0.1:5003/hospedaje/{hotel}/{habitacion}')
        dispibinilidad = response.json()
        fechas_no_disponibles = []
        for periodo in dispibinilidad:
            inicio = datetime.strptime(periodo["fecha_inicial"], "%a, %d %b %Y %H:%M:%S %Z")
            fin = datetime.strptime(periodo["fecha_final"], "%a, %d %b %Y %H:%M:%S %Z")
            delta = timedelta(days=1) 
        # Generar rango de fechas
            while inicio <= fin:
                fechas_no_disponibles.append(inicio.strftime("%Y-%m-%d"))
                inicio += delta
        print(fechas_no_disponibles)
        datos=[habitacion,hotel]
        return render_template('xd.html', dispibinilidad=fechas_no_disponibles,datos=datos)
@app.route('/formulario_enviado')
def formulario_enviado():
    print(session)
    return render_template('formulario_enviado.html')
@app.route('/perfil')
def perfil():
    print(session)
    return render_template('perfil.html')
@app.route('/perfil/<dni>/hoteles')
def hoteles_dni(dni):
    print(session)
    url = f"http://127.0.0.1:5003/hoteles/1/{dni}"
    datos={}
    print(url)
    response = requests.get(url)
    datos = response.json()
    print(datos)
    return render_template ('mis_hoteles.html',datos=datos)
@app.route("/iniciar_sesion",methods = ["POST","GET"])
def iniciar_sesion():
    session.permanent = False 
    if request.method == 'POST':
        email = request.form.get("email")
        print("email",email)
        contraseña = request.form.get("contraseña")
        url = "http://127.0.0.1:5003/iniciar_sesion"
        datos={"email":email,"contraseña":contraseña
        }
        response = requests.post(url, json=datos)
        print("mensaje ",response.json)
        if response.status_code == 200:
            print("hola")
            datos = response.json()
            print(datos[1]['email'])
            session['usuario'] = datos[1]
            print("sesion",session['usuario'])
            return redirect(url_for('formulario_enviado'))
        else:
            return render_template('inicio.html')
    else:
            return render_template('inicio.html')
@app.route("/cerrar_sesion")
def cerrar_sesion():
    print(session)
    if 'usuario' in session:
        print("cerrar")
        session.pop('usuario', None)
        return redirect(url_for('home'))
    return redirect(url_for('home'))
@app.route('/hoteles/<nombre>/habitaciones')
def habitacion_de_hotel(nombre):
    response = requests.get(f'http://127.0.0.1:5003/hoteles/{nombre}/habitaciones')
    habitaciones = response.json()
    return render_template('rooms-tariff.html', habitaciones=habitaciones)
@app.route('/correct/<habitacion>/<hotel>',methods=["POST"])
def correcto(habitacion,hotel):
    inicio = request.form.get("inicio")
    final = request.form.get("final")
    dni = request.form.get("dni")
    url = "http://127.0.0.1:5003/hospedaje"
    datos={"habitacion":habitacion,"hotel":hotel,"fecha_inicial":inicio,"fecha_final":final,"usuario":dni
    }
    print(datos)
    response = requests.post(url, json=datos)
    if response.status_code == 200:
        return "Ok"
    else:
        return "f"
@app.route('/eliminar_reserva',methods=["GET","POST"])
def eliminar_reserva():
   if request.method == 'POST':
       dni=request.form.get("dni")
       datos={"dni":dni}
       url = f"http://127.0.0.1:5003/hospedaje/{dni}"
       requests.delete(url)
       
       return "ok"
   else:
       return render_template("eliminar.html")

if __name__ == '__main__':
    app.run(debug=True, port=5002)