from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from app import db
from app.models.produto import Produto, Venda, ItemVenda
from datetime import datetime

loja_bp = Blueprint('loja', __name__)


@loja_bp.route('/loja')
def loja():
    produtos = Produto.query.all()
    return render_template('loja.html', produtos=produtos)


@loja_bp.route('/adicionar_carrinho', methods=['POST'])
def adicionar_carrinho():
    try:
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])
        
        produto = Produto.query.get(produto_id)
        if not produto:
            flash('Produto não encontrado!', 'error')
            return redirect(url_for('loja.loja'))
        
        if produto.quantidade_estoque < quantidade:
            flash('Quantidade em estoque insuficiente!', 'error')
            return redirect(url_for('loja.loja'))
        
        
        if 'carrinho' not in session:
            session['carrinho'] = []
        
        
        carrinho = session['carrinho']
        for item in carrinho:
            if item['produto_id'] == produto_id:
                item['quantidade'] += quantidade
                break
        else:
            carrinho.append({
                'produto_id': produto_id,
                'nome': produto.nome,
                'preco': float(produto.preco),
                'quantidade': quantidade,
                'imagem': produto.imagem
            })
        
        session['carrinho'] = carrinho
        session.modified = True
        
        flash('Produto adicionado ao carrinho!', 'success')
        return redirect(url_for('loja.loja'))
        
    except Exception as e:
        flash(f'Erro ao adicionar produto: {str(e)}', 'error')
        return redirect(url_for('loja.loja'))


@loja_bp.route('/carrinho')
def carrinho():
    carrinho_itens = session.get('carrinho', [])
    total = sum(item['preco'] * item['quantidade'] for item in carrinho_itens)
    return render_template('carrinho.html', carrinho_itens=carrinho_itens, total=total)


@loja_bp.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    try:
        carrinho_itens = session.get('carrinho', [])
        if not carrinho_itens:
            flash('Carrinho vazio!', 'error')
            return redirect(url_for('loja.carrinho'))
        
        
        total = sum(item['preco'] * item['quantidade'] for item in carrinho_itens)
        
        
        nova_venda = Venda(total=total, status='pendente')
        db.session.add(nova_venda)
        db.session.flush()  
        
        
        for item in carrinho_itens:
            produto = Produto.query.get(item['produto_id'])
            
            
            if produto.quantidade_estoque < item['quantidade']:
                db.session.rollback()
                flash(f'Estoque insuficiente para {produto.nome}!', 'error')
                return redirect(url_for('loja.carrinho'))
            
            
            produto.quantidade_estoque -= item['quantidade']
            
            
            item_venda = ItemVenda(
                venda_id=nova_venda.id,
                produto_id=item['produto_id'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco']
            )
            db.session.add(item_venda)
        
        db.session.commit()
        
        
        session['carrinho'] = []
        session.modified = True
        
        flash('Compra realizada com sucesso!', 'success')
        return redirect(url_for('loja.loja'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao finalizar compra: {str(e)}', 'error')
        return redirect(url_for('loja.carrinho'))


@loja_bp.route('/remover_carrinho/<int:index>')
def remover_carrinho(index):
    try:
        carrinho = session.get('carrinho', [])
        if 0 <= index < len(carrinho):
            carrinho.pop(index)
            session['carrinho'] = carrinho
            session.modified = True
            flash('Item removido do carrinho!', 'success')
        else:
            flash('Item não encontrado no carrinho!', 'error')
    except Exception as e:
        flash(f'Erro ao remover item: {str(e)}', 'error')
    
    return redirect(url_for('loja.carrinho'))