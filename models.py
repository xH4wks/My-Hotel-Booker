from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Utente(db.Model):
    codice_fiscale = db.Column(db.String(16), primary_key=True)  # PK
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    data_nascita = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    prenotazioni = db.relationship('Prenotazione', backref='utente', lazy=True)

class Hotel(db.Model):
    indirizzo = db.Column(db.String(255), primary_key=True)  # PK
    nome = db.Column(db.String(150), nullable=False)
    stelle = db.Column(db.Integer, nullable=False)
    catena = db.Column(db.String(100), nullable=True)
    descrizione = db.Column(db.Text, nullable=True)
    camere = db.relationship('Camera', backref='hotel', lazy=True)

class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_indirizzo = db.Column(db.String(255), db.ForeignKey('hotel.indirizzo'), nullable=False)  # FK
    metratura = db.Column(db.Integer, nullable=False)
    tipologia = db.Column(db.String(50), nullable=False)  # Suite o normale
    costo_notte = db.Column(db.Float, nullable=False)
    prenotazioni = db.relationship('Prenotazione', backref='camera', lazy=True)

class Prenotazione(db.Model):
    id = db.Column(db.String(10), primary_key=True)  # Numero identificativo a 10 cifre
    utente_cf = db.Column(db.String(16), db.ForeignKey('utente.codice_fiscale'), nullable=False)  # FK
    camera_id = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)  # FK
    data_checkin = db.Column(db.Date, nullable=False)
    data_checkout = db.Column(db.Date, nullable=False)

    # Assicuriamoci che non ci siano sovrapposizioni di date
    __table_args__ = (
        db.UniqueConstraint('camera_id', 'data_checkin', 'data_checkout', name='unique_prenotazione'),
    )
