window.onload = function() {
  iniciar_mapa();
};

function mostrarhoteles(map) {
  fetch('/coordenadas')
    .then(response => response.json())
    .then(data => {
      data.forEach(coord => {
        // Usamos 'latitud' y 'longitud' del JSON recibido
        const marcador = new google.maps.Marker({
          position: { lat: coord.latitud, lng: coord.longitud },  // Aseguramos que se pasen correctamente las coordenadas
          map: map
        });

        // Opcional: Agregar un mensaje al hacer clic en el marcador
        const infoWindow = new google.maps.InfoWindow({
          content: `<p>Latitud: ${coord.latitud}, Longitud: ${coord.longitud}</p>`
        });

        marcador.addListener("click", () => {
          infoWindow.open(map, marcador);
        });
      });
    })
    .catch(error => console.error('Error al obtener coordenadas:', error));
}


function iniciar_mapa() {
  let coord = { lat: -34.617159693870356, lng: -58.36835771804795 };
  let map = new google.maps.Map(document.getElementById("Mapa"), {
    zoom: 19,
    center: coord
  });
  dibujacirculo(map, coord);
  mostrarhoteles(map);

}
function dibujacirculo(map, coord) {
  const circleOptions = {
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 1,
    map: map,
    center: coord,
    radius: 80000
  }
  const circle = new google.maps.Circle(circleOptions);
  return circle;
}

iniciar_mapa();