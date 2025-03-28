// Funzione per gestire l'invio del modulo di prenotazione
document.getElementById("formPrenotazione").addEventListener("submit", function (event) {
    event.preventDefault(); // Impedisce l'invio del modulo di default

    // Raccogli i dati del modulo
    const formData = new FormData(document.getElementById("formPrenotazione"));
    
    // Creiamo un oggetto con i dati del modulo
    const data = {
        camera_id: formData.get('camera_id'),
        data_checkin: formData.get('data_checkin'),
        data_checkout: formData.get('data_checkout'),
        nome: formData.get('nome'),
        cognome: formData.get('cognome'),
        email: formData.get('email'),
        utente_cf: formData.get('utente_cf')
    };

    // Invia la richiesta POST al server
    fetch('/api/effettua_prenotazione', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Convertiamo l'oggetto in formato JSON
    })
    .then(response => response.json())
    .then(data => {
        // Quando la prenotazione è stata effettuata con successo
        console.log('Prenotazione effettuata:', data);
        
        // Mostra il modale con le informazioni della prenotazione
        document.getElementById("idPrenotazione").textContent = data.id;
        document.getElementById("nomeUtente").textContent = data.utente_cf;
        document.getElementById("numeroCamera").textContent = data.camera_id;
        document.getElementById("checkin").textContent = data.data_checkin;
        document.getElementById("checkout").textContent = data.data_checkout;

        // Mostra il modale
        document.getElementById("modale").style.display = "block";
    })
    .catch(error => {
        // In caso di errore nella richiesta
        console.error('Si è verificato un errore:', error);
    });
});

// Gestisce la chiusura del modale
document.getElementById("chiudiModale").addEventListener("click", function () {
    document.getElementById("modale").style.display = "none";
});

document.getElementById("chiudiBtn").addEventListener("click", function () {
    document.getElementById("modale").style.display = "none";
});
