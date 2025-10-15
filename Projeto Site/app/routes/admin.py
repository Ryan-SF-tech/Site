from flask import Blueprint, render_template, redirect, flash, request
import json, ast

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/adm")
def adm():
    with open("usuarios.json") as usuariosTempo:
        usuarios = json.load(usuariosTempo)
    return render_template("admnistrador.html", usuarios=usuarios)

@admin_bp.route("/excluirUsuario", methods=["POST"])
def excluirUsuario():
    usuario = request.form.get("usuarioPexcluir")
    UsuarioDICT = ast.literal_eval(usuario)
    nome = UsuarioDICT["nome"]

    with open("usuarios.json") as usuariosTempo:
        usuariosJson = json.load(usuariosTempo)
        if UsuarioDICT in usuariosJson:
            usuariosJson.remove(UsuarioDICT)
            with open("usuarios.json", "w") as f:
                json.dump(usuariosJson, f, indent=4)

    flash(f"{nome} excluído")
    return redirect("/adm")
