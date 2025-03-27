
from flask import Flask, render_template, request, jsonify
from config import Config
from models import db
from models import Utente, Camera, Prenotazione
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
# Creazione del database
with app.app_context():
    db.create_all()


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
    # Puoi usare id_camera per recuperare i dettagli della camera dal database o da un'altra fonte
    # Ad esempio: camera = get_camera_by_id(id_camera)
    return render_template('dettaglio_camera.html', id_camera=id_camera)



#ENDPOINT FUNZIONALI(API VERE)
@app.route('/api/camere')
def get_camere():
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")
    suite = request.args.get("suite") == "true"

    # Simuliamo un database di camere
    camere = [
        {"id": 1, "nome": "Camera Deluxe", "prezzo": 120, "capacita": 2, "suite": False},
        {"id": 2, "nome": "Suite Presidenziale", "prezzo": 250, "capacita": 4, "suite": True},
        {"id": 3, "nome": "Camera Standard", "prezzo": 80, "capacita": 2, "suite": False}
    ]

    # Filtriamo per suite se selezionato
    if suite:
        camere = [camera for camera in camere if camera["suite"]]

    return jsonify(camere)

# Prenotare una stanza
@app.route('/prenotazione', methods=['POST'])
def prenotare_stanza():
    data = request.json
    nuova_prenotazione = Prenotazione(
        utente_id=data['utente_id'],
        stanza_id=data['stanza_id'],
        data_checkin=datetime.strptime(data['data_checkin'], '%Y-%m-%d'),
        data_checkout=datetime.strptime(data['data_checkout'], '%Y-%m-%d')
    )
    db.session.add(nuova_prenotazione)
    db.session.commit()
    return jsonify({'message': 'Prenotazione effettuata con successo!'}), 201

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


if __name__ == '__main__':
    app.run(debug=True)