from models import db, Camera, Hotel

def populate_database():
    if not Camera.query.first():  # Evita di inserire duplicati
        print("Popolamento del database in corso...")

        # Creiamo un hotel di esempio
        hotel = Hotel(
            indirizzo="Via Napoli 1, 80016, Napoli",
            nome="Hotel Lux",
            stelle=5,
            catena="Luxury Hotels",
            descrizione="Un hotel di lusso con camere spaziose."
        )
        db.session.add(hotel)
        db.session.commit()

        # Creiamo camere statiche
        camere = [
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=25, tipologia="Standard", costo_notte=80),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=30, tipologia="Standard", costo_notte=90),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=35, tipologia="Deluxe", costo_notte=120),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=40, tipologia="Deluxe", costo_notte=130),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=45, tipologia="Suite", costo_notte=180),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=50, tipologia="Suite", costo_notte=200),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=55, tipologia="Suite", costo_notte=220),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=60, tipologia="Luxury Suite", costo_notte=300),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=65, tipologia="Luxury Suite", costo_notte=350),
            Camera(hotel_indirizzo="Via Napoli 1, 80016, Napoli", metratura=70, tipologia="Penthouse Suite", costo_notte=500)
        ]

        db.session.add_all(camere)
        db.session.commit()
        print("Dati inseriti con successo!")
    else:
        print("Il database è già popolato, nessuna azione necessaria.")

# Se esegui manualmente questo file, popola il database
if __name__ == "__main__":
    from app import app
    with app.app_context():
        populate_database()
