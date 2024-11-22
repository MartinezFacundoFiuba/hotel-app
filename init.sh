#!/bin/bash
# Inicialización del entorno virtual y las dependencias

# Crear un entorno virtual
# python3.10 -m venv venv 
# En mi caso como tengo muchas versiones de python, uso la siguiente linea:
/c/Users/Facu/AppData/Local/Programs/Python/Python310/python.exe -m venv venv
# Activar el entorno virtual
# Comprobación del sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Para Git Bash en Windows
    source venv/Scripts/activate
else
    echo "Sistema operativo no soportado para la activación del entorno virtual."
    exit 1
fi

# Instalar las dependencias necesarias
pip install flask
pip install flask_sqlalchemy
pip install mysql-connector-python
pip install flask-cors
pip install requests
pip install cython
pip install kivy
pip install --upgrade buildozer

# Instalar dependencias de Kivy para Android
# Asegúrate de ejecutar estos comandos en una terminal con privilegios de administrador
# choco install openjdk17
# choco install autoconf
# choco install libtool

echo "Dependencias instaladas correctamente :)"