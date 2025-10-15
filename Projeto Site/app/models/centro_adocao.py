from app import db
from datetime import datetime

class CentroAdocao(db.Model):
    __tablename__ = 'centro_adocao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    telefone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CentroAdocao {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.nome,
            'address': self.endereco,
            'gps_coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'phone': self.telefone,
            'website': self.website
        }