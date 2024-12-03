from flask import *
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from flask_login import login_user
from flask_login import login_manager
from flask import session
import requests
app = Flask(__name__)
#-----------------------------coneccion a la base de datos-----------------------------
def set_connection():
    try:
        engine = create_engine("mysql+mysqlconnector://user1:lizi12@localhost/HOTEL")
        connection = engine.connect()
        return connection
    except SQLAlchemyError as e:
        print(f"Error de coneccion :{e}")
        return None
#------------------------------------------------------------------------------------
#-------------------------SECTOR DE ALMACENAMIENTO DE DATOS-------------------------
#---------------------------almacenar propietarios ---------------------------------
CORS(app)
@app.route("/propietario",methods = ['POST'])
def agregar_nuevo_propietario():
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query=f"""INSERT INTO PROPIETARIOS (nombre, apellido, email, contraseña, empresa) 
    VALUES ('{datos["nombre"]}','{datos["apellido"]}','{datos["email"]}','{datos["contraseña"]}','{datos["empresa"]}');"""
    try:
        result.execute(text(query))
        conn.commit() #"confirmar" cambios a la base
        conn.close() #cerrando conexion SQL
        result.close() #cerrando conexion de la base 
        return jsonify({'message':'Se ha agregado correctamente'}),200
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al enviar los datos" +str(err)}),500
#---------------------------almacenar hoteles ---------------------------------
@app.route('/hoteles', methods=['POST'])
def agregar_nuevo_hotel():
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query=f"""INSERT INTO HOTELES (nombre,provincia,ciudad,empresa) 
    VALUES ('{datos["nombre"]}','{datos["provincia"]}','{datos["ciudad"]}','{datos["empresa"]}');"""
    try:
        result.execute(text(query))
        conn.commit()
        conn.close() 
        result.close() 
        return jsonify({'message': 'Se ha agregado correctamente'}),200
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al enviar los datos" +str(err)}),500
#---------------------------almacenar habitaciones ---------------------------------
@app.route('/habitacion', methods=['POST'])
def agregar_habitacion():
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query=f"""INSERT INTO HABITACIONES (piso,habitacion,precio) 
    VALUES ('{datos["piso"]}','{datos["habitacion"]}','{datos["precio"]}');"""
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
        return jsonify({'message': 'Se ha agregado correctamente'}),200
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al enviar los datos" +str(err)}),500
#---------------------------almacenar hospedajes ---------------------------------
@app.route('/hospedaje',methods=['POST'])
def agregar_hospedaje():
    conn = set_connection()
    result = conn
    datos = request.get_json()
    print(datos)
    habitacion = int(datos['habitacion'])  # Verifica que sea convertible a entero
    hotel = datos['hotel']
    fecha_inicial = datos['fecha_inicial']
    fecha_final = datos['fecha_final']
    usuario = int(datos['usuario'])
    query=f"""INSERT INTO DISPONIBILIDAD (habitacion,hotel,fecha_inicial,fecha_final,usuario)VALUES ('{habitacion}','{hotel}','{fecha_inicial}','{fecha_final}','{usuario}');"""
    print(query)
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
        return jsonify({'message':'Se ha agregado correctamente'}),200
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al enviar los datos" +str(err)}),500
#---------------------------almacenar usuario ---------------------------------
@app.route('/usuario',methods=['POST'])
def agregar_usuario():
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query=f"""INSERT INTO USUARIOS (nombre,apellido,email,contraseña,dni) 
    VALUES ('{datos["nombre"]}','{datos["apellido"]}','{datos["email"]}','{datos["contraseña"]}','{datos["dni"]}');"""
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
        return jsonify({'message': 'Se ha agregado correctamente'}),200
    except SQLAlchemyError as err:
        return jsonify({'mensaje:': 'se a producido un error al enviar los datos' +str(err)}),500
#-------------------------SECTOR DE CONSULTA DE DATOS-------------------------
#------------------------- consulta ofertas------------------------------------
@app.route('/ofertas',methods=["GET"])
def ofertas():
    conn=set_connection()
    data=[]
    query="SELECT * FROM ofertas;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['precio_oferta'] = row.precio_oferta
        dicc['precio_real'] = row.precio_real
        dicc['hotel'] = row.hotel
        dicc['habitacion'] = row.habitacion
  
        data.append(dicc)
    return jsonify(data),200
#------------------------- consulta usuarios------------------------------------
@app.route('/usuarios',methods=["GET"])
def usuarios():
    conn=set_connection()
    data=[]
    query="SELECT * FROM USUARIOS;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['nombre'] = row.nombre
        dicc['apellido'] = row.apellido
        dicc['email'] = row.email
        dicc['contraseña'] = row.contraseña
        dicc['dni']=row.dni
        data.append(dicc)
    return jsonify(data),200
#------------------------- consulta usuarios por id------------------------------------
@app.route('/usuario/<id>',methods=["GET"])
def usuario(id):
    conn=set_connection()
    data=[]
    query=f"SELECT * FROM USUARIOS WHERE id={id};"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'id':row[0],
            'nombre':row[1],
            'apellido':row[2],
            'email':row[3],          
            'contraseña':row[4],
            'dni':row[5]
            }
            data.append(diccionario)
    return jsonify(data), 200
#------------------------- consulta habitaciones------------------------------------
@app.route('/habitaciones',methods=["GET"])
def habitaciones():
    conn=set_connection()
    data=[]
    query="SELECT * FROM HABITACIONES;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['piso'] = row.piso
        dicc['habitacion'] = row.habitacion
        dicc['precio'] = row.precio
        data.append(dicc)
    return jsonify(data),200
#------------------------- consulta habitaciones por id------------------------------------
@app.route('/habitaciones/<id>',methods=["GET"])
def habitacion(id):
    conn=set_connection()
    data=[]
    query=f"SELECT * FROM HABITACIONES WHERE id={id};"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    print(resultado)
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'id':row[0],
            'piso':row[1],
            'habitacion':row[2],
            'precio':row[3],          
            }
            data.append(diccionario)
    return jsonify(data), 200
#------------------------- consulta hoteles------------------------------------
@app.route('/hoteles',methods=["GET"])
def hoteles():
    conn=set_connection()
    data=[]
    query="SELECT * FROM HOTELES;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['nombre'] = row.nombre
        dicc['provincia'] = row.provincia
        dicc['ciudad'] = row.ciudad
        dicc['empresa'] = row.empresa
        data.append(dicc)
    print(data)
    return jsonify(data),200
#------------------------- consulta hoteles por id------------------------------------
@app.route('/hoteles/<id>',methods=["GET"])
def hotel(id):
    conn=set_connection()
    data=[]
    query=f"SELECT * FROM USUARIOS WHERE id={id};"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'id':row[0],
            'nombre':row[1],
            'provincai':row[2],
            'ciudad':row[3],          
            'empresa':row[4],
            'dni':row[5]
            }
            data.append(diccionario)
    return jsonify(data), 200
#------------------------- consulta hoteles por empresa------------------------------------
@app.route('/hoteles/<nombre>/habitaciones',methods=["GET"])
def hotel_dni(nombre):
    conn=set_connection()
    data=[]
    print(nombre)
    query = f"SELECT * FROM HABITACIONES WHERE hotel='{nombre}';"
    try:
        result= conn.execute(text(query))
        print(query)
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    print(result)
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'id':row.id,
            'piso':row.piso,
            'habitacion':row.habitacion,
            'precio':row[3],          
            'empresa':row[4],

            }
            data.append(diccionario)
    return jsonify(data), 200
#------------------------- consulta propietarios------------------------------------
@app.route('/propietarios',methods=["GET"])
def propietarios():
    conn=set_connection()
    data=[]
    query="SELECT * FROM PROPIETARIOS;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['nombre'] = row.nombre
        dicc['apellido'] = row.apellido
        dicc['email'] = row.email
        dicc['contraseña'] = row.contraseña
        dicc['empresa']=row.empresa
        data.append(dicc)
    return jsonify(data),200
#------------------------- consulta ropietarios por id------------------------------------
@app.route('/propietarios/<id>',methods=["GET"])
def propietario_perfil(id):
    conn=set_connection()
    data=[]
    query=f"SELECT * FROM PROPIETARIOS WHERE id={id};"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'id':row[0],
            'nombre':row[1],
            'apellido':row[2],
            'email':row[3],          
            'contraseña':row[4],
            'empresa':row[5]
            }
            data.append(diccionario)
    return jsonify(data), 200
#------------------------- consulta hospedajes------------------------------------
@app.route('/hospedaje',methods = ['GET'])
def hospedajes():
    conn=set_connection()
    data=[]
    query="SELECT * FROM DISPONIBILIDAD;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['habitacion'] = row.habitacion
        dicc['hotel'] = row.hotel
        dicc['fecha_inicial'] = row.fecha_inicial
        dicc['fecha_final']=row.fecha_final
        dicc['usuario']=row.usuario
        data.append(dicc)
    print(data)
    return jsonify(data),200
#------------------------- consulta hospedajes por id------------------------------------
@app.route('/hospedaje/<id>',methods=["GET"])
def hospedaje(id):
    conn=set_connection()
    data=[]
    query=f"SELECT * FROM DISPONIBILIDAD WHERE id={id};"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'id':row[0],
            'habitacion':row[1],
            'hotel':row[2],
            'fecha_inicial':row[3],          
            'fecha_final':row[4],
            'usuario':row[5]
            }
            data.append(diccionario)
    return jsonify(data), 200
#------------------------- consulta hospedajes por hotel------------------------------------
@app.route('/hospedaje/<empresa>/<habitacion>',methods=["GET"])
def hospedaje_empresa(empresa,habitacion):
    conn=set_connection()
    data=[]
    query=f"SELECT * FROM DISPONIBILIDAD WHERE hotel='{empresa}' AND habitacion ='{habitacion}';"
    print(query)
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    resultado = result.fetchall()
    if resultado != 0:
        data = []
        for row in resultado:
            diccionario = {
            'fecha_inicial':row[3],          
            'fecha_final':row[4],
            }
            data.append(diccionario)
    return jsonify(data), 200
#----------------------------SECTOR DE MODIFICACION-------------------------
#---------------------modificaciones propietario--------------------------
@app.route('/propietario/<id>', methods=['PATCH'])
def modificar_propietario(id):
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query = f"""UPDATE PROPIETARIOS SET nombre='{datos['nombre']}',apellido='{datos['apellido']}',email='{datos['email']}',contraseña = '{datos['contraseña']}',empresa='{datos['empresa']}' WHERE id={id}; """
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
    except SQLAlchemyError as err:
        print("error",err.__cause__)
#------------------------modificacion usuario ------------------
@app.route('/usuario/<id>', methods=['PATCH'])
def modificar_usuario(id):
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query = f"""UPDATE USUARIOS SET nombre='{datos['nombre']}',apellido='{datos['apellido']}',email='{datos['email']}',contraseña = '{datos['contraseña']}',dni='{datos['dni']}' WHERE id={id}; """
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
    except SQLAlchemyError as err:
        print("error",err.__cause__)
#------------------------modificar hotel---------------------
@app.route('/hoteles/<id>', methods=['PATCH'])
def modificar_hotel(id):
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query = f"""UPDATE HOTELES SET nombre='{datos['nombre']}',provincia='{datos['provincia']}',ciudad='{datos['ciudad']}',empresa = '{datos['empresa']}' WHERE id={id}; """
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
    except SQLAlchemyError as err:
        print("error",err.__cause__)
#-----------------------modificar hospedaje --------------------
@app.route('/hospedajes/<id>', methods=['PATCH'])
def modificar_hospedajes(id):
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query = f"""UPDATE DISPONIBILIDAD SET fecha='{datos['fecha']}',habitacion='{datos['habitacion']}',hotel='{datos['hotel']}',fecha_inicial = '{datos['fecha_inicial']}',fecha_final = '{datos['fecha_final']}',usuario = '{datos['usuario']}' WHERE id={id}; """
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
    except SQLAlchemyError as err:
        print("error",err.__cause__)
#-----------------------modificar habitaciones --------------------
@app.route('/habitaciones/<id>', methods=['PATCH'])
def modificar_habitaciones(id):
    conn = set_connection()
    result = conn
    datos = request.get_json()
    query = f"""UPDATE HABITACIONES SET piso='{datos['piso']}',habitacion='{datos['habitacion']}',precio='{datos['precio']}' WHERE id={id}; """
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close() 
    except SQLAlchemyError as err:
        print("error",err.__cause__)
#---------------------SECTOR DE ELIMINACIONES----------------------
#---------- eliminar hoteles ---------------------------------
@app.route('/hoteles/<id>', methods=['DELETE'])
def eliminar_hotel(id):
    conn=set_connection()
    result = conn
    query = f"DELETE FROM HOTELES WHERE id={id};"
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close()
    except SQLAlchemyError as err:
        return jsonify({'message':'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'message':'Se ha eliminado correctamente'}), 200
#---------------eliminar propietario ---------------------------
@app.route('/propietarios/<id>', methods=['DELETE'])
def eliminar_propietarios(id):
    conn=set_connection()
    result = conn
    query = f"DELETE FROM PROPIETARIOS WHERE id={id};"
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close()
    except SQLAlchemyError as err:
        return jsonify({'message':'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'message':'Se ha eliminado correctamente'}), 200
#---------------- eliminar usuario---------------------------
@app.route('/usuario/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn=set_connection()
    result = conn
    query = f"DELETE FROM USUARIOS WHERE id={id};"
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close()
    except SQLAlchemyError as err:
        return jsonify({'message':'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'message':'Se ha eliminado correctamente'}), 200

#---------------------eliminar hospedaje por dni-------------------------
@app.route('/hospedaje/<dni>', methods=['DELETE'])
def eliminar_hospedaje(dni):
    conn=set_connection()
    result = conn
    query = f"DELETE FROM DISPONIBILIDAD WHERE usuario={dni};"
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close()
    except SQLAlchemyError as err:
        return jsonify({'message':'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'message':'Se ha eliminado correctamente'}), 200
#--------------------eliminar habitacion----------------------
@app.route('/habitacion/<id>', methods=['DELETE'])
def eliminar_habitacion(id):
    conn=set_connection()
    result = conn
    query = f"DELETE FROM HABITACIONES WHERE id={id};"
    try:
        result.execute(text(query))
        conn.commit()
        conn.close()
        result.close()
    except SQLAlchemyError as err:
        return jsonify({'message':'Se ha producido un error ' + str(err.__cause__)})
    return jsonify({'message':'Se ha eliminado correctamente'}), 200
#------------------inicio de sesion ------------------------------------------------
@app.route("/iniciar_sesion", methods=["POST"])
def login():
    datos = request.get_json()
    if "email" not in datos or "contraseña" not in datos:
        return jsonify({"mensaje": "Correo o contraseña faltantes"}), 400
    conn = set_connection()
    query = f"SELECT * FROM PROPIETARIOS WHERE email = '{datos["email"]}'"  
    try:
        print((datos["email"]))
        result = conn.execute(text(query))
        resultado = result.fetchall()
        print(resultado)
        usuario = resultado
        if not  resultado:
            return jsonify({"mensaje": 'Correo o contraseña incorrectos'}), 201
        if result:
            print(resultado)
            usuario_data = {
            "id": resultado[0][0],
            "email": resultado[0][3],
            "nombre": resultado[0][1],
            "apellido": resultado[0][2] ,
           "empresa": resultado[0][5],
            "contraseña":resultado[0][4],
            "dni": resultado[0][6]
        }
            return jsonify({'message':'Se ha agregado correctamente'},usuario_data),200
        else:
            return jsonify({"mensaje": 'Correo o contraseña incorrectos'}), 402

    except SQLAlchemyError as err:
        return jsonify({'mensaje': 'Se ha producido un error al recibir los datos: ' + str(err)}), 500
    finally:
        conn.close()
@app.route("/coordenadas")
def coordenadas():
    conn=set_connection()
    data=[]
    query="SELECT * FROM HOTELES;"
    try:
        result= conn.execute(text(query))
    except SQLAlchemyError as err:
        return jsonify({'mensaje:':"se a producido un error al recibir los datos" +str(err)}),500
    for row in result:
        dicc = {}
        dicc['latitud'] = row.latitud
        dicc['longitud'] = row.longitud
        data.append(dicc)
    print(data)
    return jsonify(data),200
if __name__ == '__main__':
   app.run("127.0.0.1",debug=True, port=5003
           )

