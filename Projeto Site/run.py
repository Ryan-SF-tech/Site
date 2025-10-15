from app import create_app, db
from app.models.administrador import Administrador  
from app.models.Usuario import Usuario
from app.models.centro_adocao import CentroAdocao
from app.models.produto import Produto

app = create_app()

def criar_tabelas_e_dados():
    with app.app_context():
        
        db.create_all()
        
        
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("📊 Tabelas criadas:", tables)

def criar_administrador():
    with app.app_context():
        
        admin = Administrador.query.filter_by(nome='administrador').first()
        
        if not admin:
            
            admin = Administrador(
                nome='administrador',
                email='admin@pet.com',  
                senha='admin123'  
            )
            db.session.add(admin)
            db.session.commit()
            print("👑 Administrador criado na tabela ADMINISTRADOR!")
        else:
            print("✅ Administrador já existe")

def criar_produtos_exemplo():
    with app.app_context():
        if Produto.query.count() == 0:
            produtos = [
                Produto(
                    nome="Ração Premium para Cães",
                    descricao="Ração nutritiva para cães adultos",
                    preco=120.50,
                    quantidade_estoque=50,
                    categoria="ração"
                ),
                Produto(
                    nome="Brinquedo para Gatos",
                    descricao="Bolinha com penas divertida",
                    preco=25.90,
                    quantidade_estoque=100,
                    categoria="brinquedo"
                ),
                Produto(
                    nome="Coleira Ajustável",
                    descricao="Coleira confortável e segura",
                    preco=35.00,
                    quantidade_estoque=30,
                    categoria="acessório"
                ),
                Produto(
                    nome="Shampoo para Pets",
                    descricao="Shampoo hipoalergênico",
                    preco=28.75,
                    quantidade_estoque=40,
                    categoria="higiene"
                )
            ]
            for produto in produtos:
                db.session.add(produto)
            db.session.commit()
            print("✅ Produtos de exemplo criados!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        criar_administrador()
        criar_produtos_exemplo()
        print("✅ Banco de dados criado com sucesso!")
        print("🚀 Servidor iniciando...")
    app.run(debug=True)