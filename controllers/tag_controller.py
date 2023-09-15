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