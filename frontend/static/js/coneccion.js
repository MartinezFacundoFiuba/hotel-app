/*coneccion para agregar propietario */
document.getElementById('formpropietario').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('http://127.0.0.1:5002/propietario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message.includes('Se ha agregado correctamente')) {
            window.location.href = 'formulario_enviado';
        } else {
            alert('Error al enviar los datos: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al enviar los datos');
    });
});
/*coneccion para agregar usuario */
document.getElementById('formusuario').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('http://127.0.0.1:5002/usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message.includes('Se ha agregado correctamente')) {
            window.location.href = 'formulario_enviado';
        } else {
            alert('Error al enviar los datos: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al enviar los datos');
    });
});
/*coneccion para agregar hotel */
document.getElementById('formhotel').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('http://127.0.0.1:5002/hoteles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message.includes('Se ha agregado correctamente')) {
            window.location.href = 'formulario_enviado';
        } else {
            alert('Error al enviar los datos: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al enviar los datos');
    });
});
/*coneccion para agregar hospedaje*/
document.getElementById('formhospedaje').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('http://127.0.0.1:5002/hospedaje', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message.includes('Se ha agregado correctamente')) {
            window.location.href = 'formulario_enviado';
        } else {
            alert('Error al enviar los datos: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al enviar los datos');
    });
});
/*coneccion para agregar habitacion */
document.getElementById('formhabitacion').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('http://127.0.0.1:5002/habitacion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message.includes('Se ha agregado correctamente')) {
            window.location.href = 'formulario_enviado';
        } else {
            alert('Error al enviar los datos: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al enviar los datos');
    });
});
/*coneccion para inicio de sesion usuario */
document.getElementById('iniciar_sesion').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('http://127.0.0.1:5002/iniciar_sesion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.message.includes('Inicio de sesion exitoso')) {
             /* deberia ir al inicio con sesion iniciada */
            window.location.href = 'formulario_enviado';

        } else {
            /*mensaje de correo o contraseña incorrecta*/
            alert('Error al iniciar sesion:' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(' Error al enviar los datos');
    });
});