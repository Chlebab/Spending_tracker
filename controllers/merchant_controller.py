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

@merchants_blueprint.route("/merchants/<id>")
def show(id):
    merchant = Merchant.query.get(id)
    tags = Tag.query.join(Transaction).filter(Transaction.merchant_id == id)
    return render_template("merchants/show.jinja", merchant=merchant, tags=tags)

@merchants_blueprint.route("/merchants/new", methods=["GET"])
def new_merchant_form():
    return render_template("merchants/new_merchant.jinja")

@merchants_blueprint.route("/merchants/new", methods=["POST"])
def add_new_merchant():
    merchant_name = request.form["name"]    
    merchant_to_save = Merchant(name=merchant_name)
    db.session.add(merchant_to_save)
    db.session.commit()
    return redirect("/merchants")  