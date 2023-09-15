from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from app import db

merchants_blueprint = Blueprint("merchants", __name__)

@merchants_blueprint.route("/merchants")
def merchants():
    merchants = Merchant.query.all()
    return render_template("merchants/index.jinja", merchants = merchants)

# @users_blueprint.route("/users/<id>")
# def show(id):
#     user = User.query.get(id)
#     locations = Location.query.join(Visit).filter(Visit.user_id == id)
#     return render_template("users/show.jinja", user=user, locations=locations)
