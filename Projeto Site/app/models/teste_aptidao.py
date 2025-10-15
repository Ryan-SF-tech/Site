from app import db
from datetime import datetime

class TesteAptidao(db.Model):
    __tablename__ = 'teste_aptidao'
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    total_sim = db.Column(db.Integer, nullable=False)
    data_teste = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TesteAptidao {self.nome_usuario}: {self.total_sim}/15>'