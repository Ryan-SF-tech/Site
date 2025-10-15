from flask import Blueprint, request, jsonify
from app import db
from app.models.teste_aptidao import TesteAptidao

teste_bp = Blueprint('teste', __name__)

@teste_bp.route('/salvar_resultado_teste', methods=['POST'])
def salvar_resultado_teste():
    try:
        data = request.get_json()
        nome_usuario = data.get('nome_usuario')
        total_sim = data.get('total_sim')
        
        if not nome_usuario:
            return jsonify({'success': False, 'message': 'Nome do usuário é obrigatório'})
        
        novo_resultado = TesteAptidao(
            nome_usuario=nome_usuario,
            total_sim=total_sim
        )
        db.session.add(novo_resultado)
        db.session.commit()
        
        print("✅ Resultado salvo no banco!")
        return jsonify({'success': True, 'message': 'Resultado salvo com sucesso!'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})