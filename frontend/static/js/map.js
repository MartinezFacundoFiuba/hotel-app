function iniciar_mapa() {
    const id = document.getElementById("mapa").getAttribute("name");
    fetch(`http://127.0.0.1:5002/hoteles/${id}`)
    .then(response => response.json())
    .then(data => {
        const latitud = parseFloat(data[0].latitud);
        const longitud = parseFloat(data[0].longitud);
        const coord = { lat: latitud, lng: longitud };
        const map = new google.maps.Map(document.getElementById("mapa"), {
            zoom: 12,
            center: coord
        });
        const marcador = new google.maps.Marker({
            position: { lat: latitud, lng: longitud },
            map: map
        });
    });
}

window.onload = iniciar_mapa;