document.addEventListener('DOMContentLoaded', function() {
    const calendar = document.getElementById('calendar');
    const reserveButton = document.getElementById('reserveButton');
    const currentDate = new Date();
    let selectedDates = [];

    // Generar días del mes
    for (let i = 1; i <= 31; i++) {
        const day = document.createElement('div');
        day.classList.add('day');
        day.textContent = i;

        const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        
        if (unavailableDays.some(d => d.date === dateStr)) {
            day.classList.add('unavailable');
        }

        day.addEventListener('click', function() {
            if (!day.classList.contains('unavailable')) {
                day.classList.toggle('selected');
                const index = selectedDates.indexOf(dateStr);
                if (index > -1) {
                    selectedDates.splice(index, 1);
                } else {
                    selectedDates.push(dateStr);
                }
            }
        });

        calendar.appendChild(day);
    }

    // Enviar fechas seleccionadas al servidor
    reserveButton.addEventListener('click', function() {
        fetch('http://127.0.0.1:5003/hospedaje', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selected_dates: selectedDates })
        }).then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  alert('Reservas realizadas con éxito');
              } else {
                  alert('Error al realizar las reservas');
              }
          });
    });
});
