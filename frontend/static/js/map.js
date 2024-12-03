function iniciar_mapa() {
  const coord = { lat: -34.617159693870356, lng: -58.36835771804795 };
  const map = new google.maps.Map(document.getElementById("mapa"), {
    zoom: 12,
    center: coord
  });
  mostrarhoteles(map);
}
function mostrarhoteles(map) {
  fetch('http://127.0.0.1:5003/coordenadas')
    .then(response => response.json())
    .then(coordenadas => {
      fetch('http://127.0.0.1:5003/hoteles')
        .then(infoResponse => infoResponse.json())
        .then(infoData => {
          coordenadas.forEach(coord => {
            const lat = parseFloat(coord.latitud);
            const lng = parseFloat(coord.longitud);
            const informacion = infoData.find(hotel => hotel.id === coord.id);
            const marcador = new google.maps.Marker({
              position: { lat: lat, lng: lng },
              map: map
            });
            const contentString = `
              <div>
                <h3>${informacion.nombre}</h3>
                <p>Latitud: ${lat}, Longitud: ${lng}</p>
                <p>${informacion.provincia}</p>
                <p>${informacion.ciudad}</p>
                <button onclick="window.open('${informacion.url}', '_blank')">Ir al sitio</button>
              </div>
            `;
            const infoWindow = new google.maps.InfoWindow({
              content: contentString
            });
            marcador.addListener("click", () => {
              infoWindow.open(map, marcador);
            });
          });
        })
        .catch(error => console.error('Error al obtener información de hoteles:', error));
    })
    .catch(error => console.error('Errorr al obtener las cooordenadas:', error));
}

window.onload = iniciar_mapa;
