from flask import Flask, render_template, url_for, redirect, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#-----------------------------coneccion a la base de datos-----------------------------
def set_connection():
    try:
        engine = create_engine("mysql+mysqlconnector://user:password@localhost/HOTEL")
        connection = engine.connect()
        print("CONECCION")
        return connection
    except SQLAlchemyError as e:
        print(f"Error de coneccion :{e}")
        return None
#------------------------------------------------------------------------------------

#-------------------------SECTOR DE ALMACENAMIENTO DE DATOS-------------------------
# Consultas SQL definidas fuera de las funciones
query_insert_propietario = """INSERT INTO PROPIETARIOS (nombre, apellido, email, contraseña, empresa) 
VALUES (:nombre, :apellido, :email, :contraseña, :empresa);"""

query_insert_hotel = """INSERT INTO HOTELES (nombre, provincia, ciudad, empresa) 
VALUES (:nombre, :provincia, :ciudad, :empresa);"""

query_insert_habitacion = """INSERT INTO HABITACIONES (piso, habitacion, precio, hotel_id) 
VALUES (:piso, :habitacion, :precio, :hotel_id);"""

query_insert_hospedaje = """INSERT INTO DISPONIBILIDAD (fecha, habitacion, hotel, fecha_inicial, fecha_final, usuario) 
VALUES (:fecha, :habitacion, :hotel, :fecha_inicial, :fecha_final, :usuario);"""

query_insert_usuario = """INSERT INTO USUARIOS (nombre, apellido, email, contraseña, dni) 
VALUES (:nombre, :apellido, :email, :contraseña, :dni);"""

query_select_usuarios = "SELECT * FROM USUARIOS;"

query_select_habitaciones = "SELECT * FROM HABITACIONES WHERE hotel_id = :hotel_id;"

query_select_habitacion = "SELECT * FROM HABITACIONES WHERE hotel_id = :hotel_id AND id = :room_id;"

query_select_hoteles = "SELECT * FROM HOTELES;"

query_select_propietarios = "SELECT * FROM PROPIETARIOS;"

query_select_hospedajes = "SELECT * FROM DISPONIBILIDAD;"

#---------------------------almacenar propietarios ---------------------------------
@app.route("/propietario", methods=['POST'])
def agregar_nuevo_propietario():
    conn = set_connection()
    datos = request.get_json()
    try:
        conn.execute(text(query_insert_propietario), datos)
        conn.commit()
        return jsonify({"mensaje": "Datos recibidos correctamente"}), 200
    except SQLAlchemyError as err:
        conn.rollback()
        return jsonify({'mensaje:': "se ha producido un error al enviar los datos: " + str(err)}), 500
    finally:
        conn.close()

#---------------------------almacenar hoteles ---------------------------------
@app.route('/hoteles', methods=['POST'])
def agregar_nuevo_hotel():
    conn = set_connection()
    datos = request.get_json()
    try:
        conn.execute(text(query_insert_hotel), datos)
        conn.commit()
        return jsonify({"mensaje": "Datos recibidos correctamente"}), 200
    except SQLAlchemyError as err:
        conn.rollback()
        return jsonify({'mensaje:': "se ha producido un error al enviar los datos: " + str(err)}), 500
    finally:
        conn.close()

#---------------------------almacenar habitaciones ---------------------------------
@app.route('/habitacion', methods=['POST'])
def agregar_habitacion():
    conn = set_connection()
    datos = request.get_json()
    try:
        conn.execute(text(query_insert_habitacion), datos)
        conn.commit()
        return jsonify({"mensaje": "Datos recibidos correctamente"}), 200
    except SQLAlchemyError as err:
        conn.rollback()
        return jsonify({'mensaje:': "se ha producido un error al enviar los datos: " + str(err)}), 500
    finally:
        conn.close()

#---------------------------almacenar hospedajes ---------------------------------
@app.route('/hospedaje', methods=['POST'])
def agregar_hospedaje():
    conn = set_connection()
    datos = request.get_json()
    try:
        conn.execute(text(query_insert_hospedaje), datos)
        conn.commit()
        return jsonify({"mensaje": "Datos recibidos correctamente"}), 200
    except SQLAlchemyError as err:
        conn.rollback()
        return jsonify({'mensaje:': "se ha producido un error al enviar los datos: " + str(err)}), 500
    finally:
        conn.close()

#---------------------------almacenar usuario ---------------------------------
@app.route('/usuario', methods=['POST'])
def agregar_usuario():
    conn = set_connection()
    datos = request.get_json()
    try:
        conn.execute(text(query_insert_usuario), datos)
        conn.commit()
        return jsonify({"mensaje": "Datos recibidos correctamente"}), 200
    except SQLAlchemyError as err:
        conn.rollback()
        return jsonify({'mensaje:': "se ha producido un error al enviar los datos: " + str(err)}), 500
    finally:
        conn.close()

#-------------------------SECTOR DE CONSULTA DE DATOS-------------------------


#------------------------- consulta usuarios------------------------------------
@app.route('/usuarios', methods=["GET"])
def usuarios():
    conn = set_connection()
    data = []
    try:
        result = conn.execute(text(query_select_usuarios))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': "se ha producido un error al recibir los datos: " + str(err)}), 500
    for row in result:
        dicc = {}
        dicc['id'] = row.id
        dicc['nombre'] = row.nombre
        dicc['apellido'] = row.apellido
        dicc['email'] = row.email
        dicc['contraseña'] = row.contraseña
        dicc['dni'] = row.dni
        data.append(dicc)
    return jsonify(data), 200

#------------------------- consulta habitaciones------------------------------------
@app.route('/habitaciones/<int:hotel_id>', methods=["GET"])
def habitaciones(hotel_id):
    conn = set_connection()
    data = []
    try:
        result = conn.execute(text(query_select_habitaciones), {"hotel_id":hotel_id})
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': "se ha producido un error al recibir los datos: " + str(err)}), 500
    for row in result:
        dicc = {}
        dicc['id'] = row.id
        dicc['piso'] = row.piso
        dicc['habitacion'] = row.habitacion
        dicc['precio'] = row.precio
        dicc['hotel_id'] = row.hotel_id
        data.append(dicc)
    return jsonify(data), 200

#------------------------- consulta habitaciones------------------------------------
@app.route('/habitaciones/<int:hotel_id>/<int:room_id>', methods=["GET"])
def habitacion_detalles(hotel_id, room_id):
    conn = set_connection()
    data = []
    try:
        result = conn.execute(text(query_select_habitacion), {"hotel_id":hotel_id, "room_id":room_id})
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': "se ha producido un error al recibir los datos: " + str(err)}), 500
    for row in result:
        dicc = {}
        dicc['id'] = row.id
        dicc['piso'] = row.piso
        dicc['habitacion'] = row.habitacion
        dicc['precio'] = row.precio
        dicc['hotel_id'] = row.hotel_id
        data.append(dicc)
    return jsonify(data), 200

#------------------------- consulta hoteles------------------------------------
@app.route('/hoteles', methods=["GET"])
def hoteles():
    conn = set_connection()
    data = []
    try:
        result = conn.execute(text(query_select_hoteles))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': "se ha producido un error al recibir los datos: " + str(err)}), 500
    for row in result:
        dicc = {}
        dicc['id'] = row.id
        dicc['nombre'] = row.nombre
        dicc['provincia'] = row.provincia
        dicc['ciudad'] = row.ciudad
        dicc['empresa'] = row.empresa
        data.append(dicc)
    return jsonify(data), 200

#------------------------- consulta propietarios------------------------------------
@app.route('/propietarios', methods=["GET"])
def propietarios():
    conn = set_connection()
    data = []
    try:
        result = conn.execute(text(query_select_propietarios))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': "se ha producido un error al recibir los datos: " + str(err)}), 500
    for row in result:
        dicc = {}
        dicc['id'] = row.id
        dicc['nombre'] = row.nombre
        dicc['apellido'] = row.apellido
        dicc['email'] = row.email
        dicc['contraseña'] = row.contraseña
        dicc['empresa'] = row.empresa
        data.append(dicc)
    return jsonify(data), 200

#------------------------- consulta hospedajes------------------------------------
@app.route('/hospedaje', methods=['GET']) 
def hospedajes():
    conn = set_connection()
    data = []
    try:
        result = conn.execute(text(query_select_hospedajes))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': "se ha producido un error al recibir los datos: " + str(err)}), 500
    for row in result:
        dicc = {}
        dicc['id'] = row.id
        dicc['fecha'] = row.fecha
        dicc['habitacion'] = row.habitacion
        dicc['hotel'] = row.hotel
        dicc['fecha_inicial'] = row.fecha_inicial
        dicc['fecha_final'] = row.fecha_final
        dicc['usuario'] = row.usuario
        dicc['estado'] = row.estado
        data.append(dicc)
    return jsonify(data), 200

#----------------------------SECTOR DE MODIFICACION-------------------------

#---------------------modificaciones propietario--------------------------
@app.route('/propietario/<id>', methods=['PATCH'])
def modificar_propietario(id):
    conn = set_connection()
    datos = request.get_json()
    query = f"""UPDATE PROPIETARIOS SET nombre='{datos['nombre']}', apellido='{datos['apellido']}', email='{datos['email']}', contraseña='{datos['contraseña']}', empresa='{datos['empresa']}' WHERE id={id};"""
    try:
        conn.execute(text(query))
        conn.commit()
        return jsonify({"mensaje": "Propietario modificado correctamente."}), 200  
    except SQLAlchemyError as err:
        print("Error al modificar propietario:", err.__cause__)  
        return jsonify({"mensaje": "Error al modificar propietario."}), 500 

#------------------------modificacion usuario ------------------
@app.route('/usuario/<id>', methods=['PATCH'])
def modificar_usuario(id):
    conn = set_connection()
    datos = request.get_json()
    query = f"""UPDATE USUARIOS SET nombre='{datos['nombre']}', apellido='{datos['apellido']}', email='{datos['email']}', contraseña='{datos['contraseña']}', dni='{datos['dni']}' WHERE id={id};"""
    try:
        conn.execute(text(query))
        conn.commit()
        return jsonify({"mensaje": "Usuario modificado correctamente."}), 200  
    except SQLAlchemyError as err:
        print("Error al modificar usuario:", err.__cause__)  
        return jsonify({"mensaje": "Error al modificar usuario."}), 500 

#------------------------modificar hotel---------------------
@app.route('/hoteles/<id>', methods=['PATCH'])
def modificar_hotel(id):
    conn = set_connection()
    datos = request.get_json()
    query = f"""UPDATE HOTELES SET nombre='{datos['nombre']}', provincia='{datos['provincia']}', ciudad='{datos['ciudad']}', empresa='{datos['empresa']}' WHERE id={id};"""
    try:
        conn.execute(text(query))
        conn.commit()
        return jsonify({"mensaje": "Hotel modificado correctamente."}), 200  
    except SQLAlchemyError as err:
        print("Error al modificar hotel:", err.__cause__)  
        return jsonify({"mensaje": "Error al modificar hotel."}), 500 

#-----------------------modificar hospedaje --------------------
@app.route('/hospedajes/<id>', methods=['PATCH'])
def modificar_hospedajes(id):
    conn = set_connection()
    datos = request.get_json()
    query = f"""UPDATE DISPONIBILIDAD SET fecha='{datos['fecha']}', habitacion='{datos['habitacion']}', hotel='{datos['hotel']}', fecha_inicial='{datos['fecha_inicial']}', fecha_final='{datos['fecha_final']}', usuario='{datos['usuario']}', estado='{datos['estado']}' WHERE id={id};"""
    try:
        conn.execute(text(query))
        conn.commit()
        return jsonify({"mensaje": "Hospedaje modificado correctamente."}), 200  
    except SQLAlchemyError as err:
        print("Error al modificar hospedaje:", err.__cause__)  
        return jsonify({"mensaje": "Error al modificar hospedaje."}), 500 

#-----------------------modificar habitaciones --------------------
@app.route('/habitaciones/<id>', methods=['PATCH'])
def modificar_habitaciones(id):
    conn = set_connection()
    datos = request.get_json()
    query = f"""UPDATE HABITACIONES SET piso='{datos['piso']}', habitacion='{datos['habitacion']}', precio='{datos['precio']}' WHERE id={id};"""
    try:
        conn.execute(text(query))
        conn.commit()
        return jsonify({"mensaje": "Habitacion modificada correctamente."}), 200  
    except SQLAlchemyError as err:
        print("Error al modificar habitacion:", err.__cause__)  
        return jsonify({"mensaje": "Error al modificar habitacion."}), 500 

#---------------------SECTOR DE ELIMINACIONES----------------------
#---------- eliminar hoteles ---------------------------------
@app.route('/hoteles/<id>', methods=['DELETE'])
def eliminar_hotel(id):
    conn = set_connection()
    try:
        query_delete_disponibilidad = f"DELETE FROM DISPONIBILIDAD WHERE hotel={id};"
        conn.execute(text(query_delete_disponibilidad))
        
        query_delete_habitaciones = f"DELETE FROM HABITACIONES WHERE hotel_id={id};"
        conn.execute(text(query_delete_habitaciones))
        
        query = f"DELETE FROM HOTELES WHERE id={id};"
        conn.execute(text(query))
        conn.commit()
    except SQLAlchemyError as err:
        return jsonify({'mensaje': 'Se ha producido un error: ' + str(err.__cause__)}), 500
    
    return jsonify({'mensaje': 'Se ha eliminado correctamente'}), 200

#---------------eliminar propietario ---------------------------
@app.route('/propietarios/<id>', methods=['DELETE'])
def eliminar_propietarios(id):
    conn = set_connection()
    query = f"DELETE FROM PROPIETARIOS WHERE id={id};"
    try:
        conn.execute(text(query))
        conn.commit()
    except SQLAlchemyError as err:
        return jsonify({'mensaje': 'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'mensaje': 'Se ha eliminado correctamente'}), 200

#---------------- eliminar usuario---------------------------
@app.route('/usuario/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = set_connection()
    query = f"DELETE FROM USUARIOS WHERE id={id};"
    try:
        conn.execute(text(query))
        conn.commit()
    except SQLAlchemyError as err:
        return jsonify({'mensaje': 'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'mensaje': 'Se ha eliminado correctamente'}), 200

#---------------------eliminar hospedaje-------------------------
@app.route('/hospedaje/<id>', methods=['DELETE']) 
def eliminar_hospedaje(id):
    conn = set_connection()
    query = f"DELETE FROM DISPONIBILIDAD WHERE id={id};"
    try:
        conn.execute(text(query))
        conn.commit()
    except SQLAlchemyError as err:
        return jsonify({'mensaje': 'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'mensaje': 'Se ha eliminado correctamente'}), 200

#--------------------eliminar habitacion----------------------
@app.route('/habitacion/<id>', methods=['DELETE'])
def eliminar_habitacion(id):
    conn = set_connection()
    query_delete_disponibilidad = f"DELETE FROM DISPONIBILIDAD WHERE habitacion={id};"
    conn.execute(text(query_delete_disponibilidad))
    query = f"DELETE FROM HABITACIONES WHERE id={id};"
    try:
        conn.execute(text(query))
        conn.commit()
    except SQLAlchemyError as err:
        return jsonify({'mensaje': 'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'mensaje': 'Se ha eliminado correctamente'}), 200

if __name__ == '__main__':
    app.run("127.0.0.1", debug=True, port=5002)

