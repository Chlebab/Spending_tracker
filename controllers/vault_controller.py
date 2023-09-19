from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from models.user import User
from models.budget import Budget
from models.vault import Vault
from app import db

vaults_blueprint = Blueprint("vaults", __name__)

@vaults_blueprint.route("/vaults")
def vaults():
    vaults = Vault.query.all()
    return render_template("vaults/index.jinja", vaults = vaults)