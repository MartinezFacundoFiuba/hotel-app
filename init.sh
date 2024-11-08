#!/bin/bash
# Inicialización del entorno virtual y las dependencias

# Crear un entorno virtual
python3 -m venv venv

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

echo "Dependencias instaladas correctamente :)"