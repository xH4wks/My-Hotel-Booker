from flask import Flask, render_template, request, jsonify
from config import Config
from models import db
from models import Utente, Camera, Prenotazione
from datetime import datetime
import random,string


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
# Creazione del database
with app.app_context():
    db.create_all()
    from populate_db import populate_database
    populate_database() 

@app.route('/home')
def home():
    return render_template('homepage.html')


@app.route('/ricerca')
def ricerca():
    return render_template('ricerca_prenotazione.html')

@app.route('/prenota')
def prenota():
    return render_template('effettua_prenotazione.html')

@app.route('/prenota/camera/<int:id_camera>')
def dettagli_camera(id_camera):
    # Recupera la camera dal database
    camera = Camera.query.get(id_camera)
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")

    if not camera:
        return jsonify({"error": "Camera non trovata"}), 404

    return render_template(
        'dettaglio_camera.html', 
        camera=camera,
        checkin =checkin,
        checkout = checkout
    )



#ENDPOINT FUNZIONALI(API VERE)
@app.route('/api/camere')
def get_camere():
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")
    suite = request.args.get("suite") == "true"
        # Filtriamo per suite se selezionato
    if suite:
        camere = Camera.query.filter(Camera.tipologia.ilike('%suite%')).order_by(Camera.costo_notte).all()
    else:
        camere = Camera.query.order_by(Camera.costo_notte).all() # Recupera tutte le camere dal database
    
    result = [
        {
            "id": camera.id,
            "hotel": camera.hotel_indirizzo,
            "metratura": camera.metratura,
            "tipologia": camera.tipologia,
            "costo_notte": camera.costo_notte
        }
        for camera in camere
    ]
    #print(camere)
    return jsonify(result)

# Funzione per generare un ID prenotazione unico
def generate_booking_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@app.route('/api/effettua_prenotazione', methods=['POST'])
def prenotazione():
 # Ricevi i dati JSON dalla richiesta
        data = request.get_json()

        print(f"Dati ricevuti: {data}")
        
        # Genera un ID prenotazione unico
        prenotazione_id = generate_booking_id()
        
        # Ottieni i dati dal form
        utente_cf = data['utente_cf']
        camera_id = data['camera_id']
        data_checkin = data['data_checkin']
        data_checkout = data['data_checkout']

        # Converto le date da stringa a oggetto date
        data_checkin = datetime.strptime(data_checkin, "%Y-%m-%d").date()
        data_checkout = datetime.strptime(data_checkout, "%Y-%m-%d").date()
        
        # Controllo se l'utente esiste
        utente = Utente.query.filter_by(codice_fiscale=utente_cf).first()
        if not utente:
            # Se l'utente non esiste, crealo
            nome = data['nome']
            cognome = data['cognome']
            email = data['email']
            utente = Utente(codice_fiscale=utente_cf, nome=nome, cognome=cognome, email=email)
            db.session.add(utente)
            db.session.commit()

        # Crea una nuova prenotazione
        new_prenotazione = Prenotazione(
            id=prenotazione_id,
            utente_cf=utente_cf,
            camera_id=camera_id,
            data_checkin=data_checkin,
            data_checkout=data_checkout
        )

        # Aggiungi la prenotazione al database
        db.session.add(new_prenotazione)
        db.session.commit()

        # Restituisci la prenotazione come risposta JSON
        return jsonify(new_prenotazione.to_dict())


# Ottenere tutte le prenotazioni
@app.route('/prenotazioni', methods=['GET'])
def get_prenotazioni():
    prenotazioni = Prenotazione.query.all()
    result = [
        {
            "id": p.id,
            "utente": p.utente.nome,
            "stanza": p.stanza.numero,
            "checkin": p.data_checkin.strftime('%Y-%m-%d'),
            "checkout": p.data_checkout.strftime('%Y-%m-%d')
        }
        for p in prenotazioni
    ]
    return jsonify(result), 200
#NON TOCCARE PER TESTARE#
# SCOMMENTARE SOLO SE SI VUOLE CANCELLARE L'INTERO DATABASE DI DATI
@app.route('/reset_db', methods=['GET'])
def reset_db():
    try:
        # Elimina tutte le tabelle
        db.drop_all()
        
        # Crea nuovamente le tabelle
        db.create_all()
        
        return "Database resettato con successo!"
    except Exception as e:
        return f"Errore durante il reset del database: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)