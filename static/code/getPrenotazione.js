function fetchResults(event) {
    event.preventDefault(); // Previene il caricamento della pagina
    
    fetch(`/api/prenotazioni`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById("results");
            resultsContainer.innerHTML = ""; // Pulisce i risultati precedenti
            
            data.forEach(prenotazione => {
                const card = document.createElement("div");
                card.classList.add("card");
                card.innerHTML = `
                    <h2>${prenotazione.id}</h2>
                    <p>Camera: ${prenotazione.camera}
                    <p>Utente: ${prenotazione.utente}</p>
                    <p>Check-in: ${prenotazione.checkin}</p>
                    <p>Check-out: ${prenotazione.checkout}</p>
                `;
                resultsContainer.appendChild(card);
            });
        })
        .catch(error => console.error("Errore nel caricamento delle camere:", error));
}
