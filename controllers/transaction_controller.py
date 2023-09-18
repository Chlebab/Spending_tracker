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
    transactions_sum = sum(transaction.amount for transaction in transactions)
    return render_template("transactions/index.jinja", transactions = transactions, transactions_sum=transactions_sum)

@transactions_blueprint.route("/transactions/<int:id>")
def show(id):
    transaction = Transaction.query.get(id)
    merchants = Merchant.query.join(Transaction).filter(Transaction.tag_id == id)
    return render_template("transactions/show_transaction.jinja", transaction=transaction, merchants=merchants)

@transactions_blueprint.route("/transactions/new", methods=['GET'])
def new_transaction_form():
    merchants = Merchant.query.all()
    tags = Tag.query.all()
    return render_template("transactions/new_transaction.jinja", merchants = merchants, tags = tags)

@transactions_blueprint.route("/transactions",  methods=['POST'])
def add_new_transaction():
    merchant_id = request.form['merchant_id']
    tag_id = request.form['tag_id']
    amount = request.form['amount']
    date = request.form['date']
    comment = request.form['comment']
    transaction = Transaction(merchant_id = merchant_id, tag_id = tag_id, amount=amount, date=date, comment=comment)
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
    merchants = Merchant.query.all()
    tags = Tag.query.all()
    return render_template("transactions/edit_transaction.jinja", transaction=transaction_to_edit, merchants=merchants, tags=tags)

@transactions_blueprint.route("/transactions/edit/<int:id>", methods = ["POST"])
def edit_transaction(id):
    transaction_to_edit = Transaction.query.get(id)

    if transaction_to_edit:
        merchant_id = request.form.get("merchant_id")
        tag_id = request.form.get("tag_id")
        amount = request.form.get("amount")
        date = request.form.get("date")
        comment = request.form.get("comment")

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

@transactions_blueprint.route("/transactions/sort/<column>")
def sort_transactions(column):
    transactions = get_transactions()
    transactions_sum = sum(transaction.amount for transaction in transactions)
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

