from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from models.budget import Budget
from app import db
import matplotlib.pyplot as plt
import io
import base64

budgets_blueprint = Blueprint("budgets", __name__)

@budgets_blueprint.route("/budgets")
def budgets():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date and end_date:
        transactions = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
    else:
        transactions = Transaction.query.all()
    transactions_sum = sum(transaction.amount for transaction in transactions)
    existing_budget = Budget.query.first()
    if existing_budget:
        budget = existing_budget
    else:
        budget = None
    all_budgets = Budget.query.all()

    
    dates = [transaction.date for transaction in transactions]
    amounts = [transaction.amount for transaction in transactions]
    budget_curve = [budget.budget_amount] * len(dates) if budget else [0] * len(dates)

    plt.figure(figsize=(10, 6))
    plt.plot(dates, budget_curve, linestyle='-', color='red', label='Budget')
    plt.bar(dates, amounts, width=0.8, label="Spending")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Spending Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    img_buf.seek(0)

    img_base64 = base64.b64encode(img_buf.read()).decode("utf-8")
    img_src = f"data:image/png;base64,{img_base64}"

    return render_template("budgets/index.jinja", budget = budget, budgets=all_budgets, transactions_sum=transactions_sum, img_src=img_src)

@budgets_blueprint.route("/budgets", methods=["POST"])
def add_budget():
    existing_budget = Budget.query.first()
    if existing_budget:
        return redirect("/budgets") 
    budget_amount = request.form['budget']
    budget = Budget(budget_amount=budget_amount)
    db.session.add(budget)
    db.session.commit()
    return redirect("/budgets")

@budgets_blueprint.route("/budgets/delete/<int:id>", methods=["POST"])
def delete_budget(id):
    budget_to_delete = Budget.query.get(id)
    if budget_to_delete:
        db.session.delete(budget_to_delete)
        db.session.commit()
    return redirect("/budgets")