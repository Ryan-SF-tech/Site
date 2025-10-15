from flask import Blueprint, render_template, request, redirect, flash
from app.models.Usuario import Usuario
import json
from app import db
usuario_bp = Blueprint("usuario", __name__)



@usuario_bp.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@usuario_bp.route("/cadastrarUsuario", methods=["POST"])
def cadastrarUsuario():
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    email = request.form['email']

    with open("usuarios.json") as usuariosTempo:
        usuarios = json.load(usuariosTempo)

    for usuario in usuarios:
        if usuario["nome"] == nome:
            flash("Usuário já existe. Escolha outro nome.")
            return redirect("/cadastro")

    usuarios.append({"nome": nome, "senha": senha, "email": email})
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=4)

    novo_usuario = Usuario(nome=nome, senha=senha, email=email)
    db.session.add(novo_usuario) 
    db.session.commit() 

    flash(f"{nome} cadastrado com sucesso!")
    return render_template("usuario.html")

@usuario_bp.route("/questionario")
def questionario():
    return render_template("questionario.html")

@usuario_bp.route("/localizacao")
def localizacao():
    return render_template("localizacao.html")
