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
    # merchants = merchants.query.join(Transaction).filter(Transaction.tag_id == id)
    return render_template("tags/show_tag.jinja", tag=tag)

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


@tags_blueprint.route("/tags/delete", methods =["POST"])
def delete_tag():
    id = request.form.get("tag_id") 
    tag_to_delete = Tag.query.get(id)
    db.session.delete(tag_to_delete)
    db.session.commit()
    return redirect("/tags")


@tags_blueprint.route("/tags/edit/<int:id>", methods=["GET"])
def edit_tag_form(id):
    tag_to_edit = Tag.query.get(id)
    return render_template("tags/edit_tag.jinja", tag=tag_to_edit)

@tags_blueprint.route("/tags/edit/<int:id>", methods = ["POST"])
def edit_tag(id):
    tag_to_edit = Tag.query.get(id)
    if tag_to_edit:
        new_tag_category = request.form.get("category")
        tag_to_edit.category = new_tag_category
        db.session.commit()
        return redirect(f"/tags")