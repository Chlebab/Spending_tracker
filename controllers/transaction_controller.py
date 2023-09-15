from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from app import db

transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/transactions")
def transactions():
    transactions = Transaction.query.all()
    return render_template("transactions/index.jinja", transactions = transactions)
