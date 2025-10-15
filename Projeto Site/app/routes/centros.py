from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import requests
from app import db
from app.models.centro_adocao import CentroAdocao

centros_bp = Blueprint('centros', __name__)


@centros_bp.route('/api/search-centers')
def search_centers():
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        
        
        todos_centros = []
        
        
        centros_db = CentroAdocao.query.all()
        for centro in centros_db:
            todos_centros.append({
                'id': centro.id,
                'title': centro.nome,
                'address': centro.endereco,
                'gps_coordinates': {
                    'latitude': centro.latitude,
                    'longitude': centro.longitude
                },
                'phone': centro.telefone,
                'website': centro.website,
                'fonte': 'banco'  
            })
        
        
        if lat and lng:  
            try:
                params = {
                    "engine": "google_maps",
                    "q": "centro de adoção de animais", 
                    "ll": f"@{lat},{lng},15z",
                    "type": "search",
                    "hl": "pt-BR",  
                    "gl": "br",      
                    "api_key": "04fa7ea9827380a90f7412fe2d4ebb09f8820c096cc3d1a2ece1c935bcff80fb"
                }
                
                response = requests.get('https://serpapi.com/search.json', params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                centros_externos = data.get('local_results', [])
                
                
                for centro in centros_externos:
                    if 'gps_coordinates' in centro:
                        todos_centros.append({
                            **centro,  
                            'fonte': 'api_externa',  
                            'icon': '🏢'  
                        })
                        
            except Exception as e:
                print(f"⚠️ API externa falhou: {e}")
                
        
        print(f"🎯 Retornando {len(todos_centros)} centros ({len(centros_db)} do banco)")
        return jsonify(todos_centros)
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return jsonify({'error': str(e)}), 500


@centros_bp.route('/admin/centros')
def admin_centros():
    centros = CentroAdocao.query.all()
    return render_template('admin_centros.html', centros=centros)


@centros_bp.route('/admin/centros/adicionar', methods=['POST'])
def adicionar_centro():
    try:
        nome = request.form['nome']
        endereco = request.form['endereco']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        telefone = request.form.get('telefone', '')
        website = request.form.get('website', '')
        
        novo_centro = CentroAdocao(
            nome=nome,
            endereco=endereco,
            latitude=latitude,
            longitude=longitude,
            telefone=telefone,
            website=website
        )
        
        db.session.add(novo_centro)
        db.session.commit()
        
        flash('Centro de adoção adicionado com sucesso!', 'success')
        return redirect(url_for('centros.admin_centros'))
        
    except Exception as e:
        flash(f'Erro ao adicionar centro: {str(e)}', 'error')
        return redirect(url_for('centros.admin_centros'))


@centros_bp.route('/admin/centros/excluir/<int:id>', methods=['POST'])
def excluir_centro(id):
    try:
        centro = CentroAdocao.query.get_or_404(id)
        db.session.delete(centro)
        db.session.commit()
        flash('Centro excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir centro: {str(e)}', 'error')
    
    return redirect(url_for('centros.admin_centros'))