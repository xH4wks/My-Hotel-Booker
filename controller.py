
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('homepage.html')


@app.route('/ricerca')
def ricerca():
    return render_template('ricerca_prenotazione.html')

@app.route('/prenota')
def prenota():
    return render_template('effettua_prenotazione.html')



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

#NON TOCCARE PER TESTARE#
if __name__ == '__main__':
    app.run(debug=True)