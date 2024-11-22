document.getElementById('formpropietario2').addEventListener('submit', function(event) {
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
        if (result.message.includes('Se ha agregado correctamente')) {
            window.location.href = 'formulario_enviado';
        } else {
            alert('Error al enviar los datos1: ' + result.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('400Error al enviar los datos');
    });
});

function iniciar_sesion(){
    let urlpropietarios = "http://127.0.0.1:5002/propietarios";
    fetch(urlpropietarios)
      .then(response => response.json())
      .then(dataCoordenadas => {

      })
      .catch(error => console.log(error));
  }
