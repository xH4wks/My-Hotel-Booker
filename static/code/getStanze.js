function fetchResults(event) {
    event.preventDefault(); // Previene il caricamento della pagina
    
    const checkin = document.getElementById("checkin").value;
    const checkout = document.getElementById("checkout").value;
    const suite = document.querySelector("input[name='suite']").checked;

    fetch(`/api/camere?checkin=${checkin}&checkout=${checkout}&suite=${suite}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById("results");
            resultsContainer.innerHTML = ""; // Pulisce i risultati precedenti
            
            data.forEach(camera => {
                const card = document.createElement("div");
                card.classList.add("card");
                card.innerHTML = `
                    <h2>${camera.tipologia}</h2>
                    <p>Prezzo: €${camera.costo_notte} a notte</p>
                    <p>Dimensione: ${camera.metratura}mq</p>
                    <button onclick="location.href='/prenota/camera/${camera.id}?checkin=${checkin}&checkout=${checkout}'">Dettagli</button>
                `;
                resultsContainer.appendChild(card);
            });
        })
        .catch(error => console.error("Errore nel caricamento delle camere:", error));
}
