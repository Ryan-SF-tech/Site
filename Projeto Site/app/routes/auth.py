from flask import Blueprint, render_template, request, redirect, flash
from app.models.Usuario import Usuario, db
import json

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    email = request.form.get("email")

    if nome == "administrador" and senha == "admin123" and email == "admin@pet.com":
        return redirect("/adm")

    usuario = Usuario.query.filter_by(nome=nome, senha=senha, email=email).first()
    if usuario:
        return render_template("usuario.html")

    flash("Usuário inválido")
    return redirect("/")
