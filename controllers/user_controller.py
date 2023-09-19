from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from models.user import User
from models.budget import Budget
from models.vault import Vault
from app import db

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/users")
def users():
    users = User.query.all()
    return render_template("users/index.jinja", users = users)

@users_blueprint.route("/users/new", methods=["GET"])
def new_user_form():
    return render_template("users/new_user.jinja")

@users_blueprint.route("/users/new", methods=["POST"])
def add_new_user():
    user_username = request.form["username"]    
    user_funds = request.form["funds"]    
    user_to_save = User(username=user_username, funds=user_funds)
    db.session.add(user_to_save)
    db.session.commit()
    return redirect("/users")

@users_blueprint.route("/users/delete", methods =["POST"])
def delete_user():
    id = request.form.get("user_id") 
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect("/users")

@users_blueprint.route("/users/edit/<int:id>", methods=["GET"])
def edit_user_form(id):
    user_to_edit = User.query.get(id)
    return render_template("users/edit_user.jinja", user=user_to_edit)

@users_blueprint.route("/users/edit/<int:id>", methods = ["POST"])
def edit_user(id):
    user_to_edit = User.query.get(id)
    if user_to_edit:
        new_user_username = request.form.get("username")
        new_user_funds = request.form.get("funds")
        user_to_edit.username = new_user_username
        user_to_edit.funds = new_user_funds
        db.session.commit()
        return redirect(f"/users")