from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from app import db

tags_blueprint = Blueprint("tags", __name__)

@tags_blueprint.route("/tags")
def tags():
    tags = Tag.query.all()
    return render_template("tags/index.jinja", tags = tags)

@tags_blueprint.route("/tags/<id>")
def show(id):
    tag = Tag.query.get(id)
    merchants = Merchant.query.join(Transaction).filter(Transaction.tag_id == id)
    return render_template("tags/show_tag.jinja", tag=tag, merchants=merchants)

@tags_blueprint.route("/tags/new", methods=["GET"])
def new_tag_form():
    return render_template("tags/new_tag.jinja")

@tags_blueprint.route("/tags/new", methods=["POST"])
def add_new_tag():
    tag_category = request.form["category"]    
    tag_to_save = Tag(category=tag_category)
    db.session.add(tag_to_save)
    db.session.commit()
    return redirect("/tags")  
