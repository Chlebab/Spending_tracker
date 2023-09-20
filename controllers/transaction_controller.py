from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from models.user import User
from models.budget import Budget
from models.vault import Vault
from app import db


transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/transactions", methods=["GET"])
def transactions():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")    
    if start_date and end_date:
        transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
    else:
        transactions = Transaction.query.all()
    budget = Budget.query.first()
    transactions_sum = sum(transaction.amount for transaction in transactions)
    
    return render_template("transactions/index.jinja", transactions = transactions, transactions_sum=transactions_sum, budget=budget)

@transactions_blueprint.route("/transactions/<int:id>")
def show(id):
    transaction = Transaction.query.get(id)
    return render_template("transactions/show_transaction.jinja", transaction=transaction)

@transactions_blueprint.route("/transactions/new", methods=['GET'])
def new_transaction_form():
    users = User.query.all()
    merchants = Merchant.query.all()
    tags = Tag.query.all()
    return render_template("transactions/new_transaction.jinja", merchants = merchants, tags = tags, users=users)

@transactions_blueprint.route("/transactions",  methods=['POST'])
def add_new_transaction():
    user_id = request.form['user_id']
    merchant_id = request.form['merchant_id']
    tag_id = request.form['tag_id']
    amount = request.form['amount']
    date = request.form['date']
    comment = request.form['comment']
    transaction = Transaction(user_id=user_id, merchant_id = merchant_id, tag_id = tag_id, amount=amount, date=date, comment=comment)
    db.session.add(transaction)
    db.session.commit()
    return redirect('/transactions')


@transactions_blueprint.route("/transactions/delete", methods =["POST"])
def delete_transaction():
    id = request.form.get("transaction_id") 
    transaction_to_delete = Transaction.query.get(id)
    db.session.delete(transaction_to_delete)
    db.session.commit()
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/edit/<int:id>", methods=["GET"])
def edit_transaction_form(id):
    transaction_to_edit = Transaction.query.get(id)
    users = User.query.all()
    merchants = Merchant.query.all()
    tags = Tag.query.all()
    return render_template("transactions/edit_transaction.jinja", transaction=transaction_to_edit, users=users, merchants=merchants, tags=tags)

@transactions_blueprint.route("/transactions/edit/<int:id>", methods = ["POST"])
def edit_transaction(id):
    transaction_to_edit = Transaction.query.get(id)
    if transaction_to_edit:
        user_id = request.form.get("user_id")
        merchant_id = request.form.get("merchant_id")
        tag_id = request.form.get("tag_id")
        amount = request.form.get("amount")
        date = request.form.get("date")
        comment = request.form.get("comment")

        transaction_to_edit.user_id = user_id
        transaction_to_edit.merchant_id = merchant_id
        transaction_to_edit.tag_id = tag_id
        transaction_to_edit.amount = amount
        transaction_to_edit.date = date
        transaction_to_edit.comment = comment

        db.session.commit()
        return redirect(f"/transactions")
    
def get_transactions():
    transactions = Transaction.query.all()
    return transactions

@transactions_blueprint.route("/transactions/sort/<column>", methods=["GET", "POST"])
def sort_transactions(column):
    transactions = get_transactions()
    transactions_sum = sum(transaction.amount for transaction in transactions)

    if column == 'user':
        transactions = sorted(transactions, key=lambda t: t.user.username)
    if column == 'merchant':
        transactions = sorted(transactions, key=lambda t: t.merchant.name)
    elif column == 'category':
        transactions = sorted(transactions, key=lambda t: t.tag.category)
    elif column == 'amount':
        transactions = sorted(transactions, key=lambda t: t.amount)
    elif column == 'date':
        transactions = sorted(transactions, key=lambda t: t.date)
    elif column == 'comment':
        transactions = sorted(transactions, key=lambda t: t.comment)
    return render_template("transactions/index.jinja", transactions=transactions, transactions_sum=transactions_sum) 

