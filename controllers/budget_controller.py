from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from models.budget import Budget
from app import db
from services.budget_services import get_transactions_sum, get_transactions, get_budget, generate_graph_img_source
import matplotlib.pyplot as plt
import io
import base64

budgets_blueprint = Blueprint("budgets", __name__)

# we can consider extracting out logic and extra verbosity from our controller functions, we care more about _what_ are code is doing as opposed to _how_ its doing it. 
# see below for example
# this has the following benefits ..

# 1. Separation of concerns
# One of the core principles of software engineering is the separation of concerns. By moving business logic out of controllers and into separate components, you ensure that each component has a single responsibility. Controllers should primarily handle user input and orchestrate the flow of data, while logic related to data manipulation, validation, and business rules should be handled by other parts of the application.
# 2. Code Reusability (keeps us DRY)
# Extracting logic into separate modules or classes makes it more reusable. You can use the same logic in multiple controllers or even in different parts of your application. This reduces code duplication and leads to a more maintainable codebase.
# 3. Scalable 
# As your application grows, you may need to change or extend its functionality, if we have to do the same action several times, it helps if we have the logic to do that action central to one place if we suddenly need to change how we are doing that action we now need to just change the code in one place as apposed to every place we where doing that action.
# 4. Readability 
# Controllers are typically responsible for managing the flow of requests and responses. When logic is mixed with controller code, it can make controllers bulky and less readable. Extracting logic into separate files/folders leads to cleaner, more focused, and more readable code. This improves the overall maintainability of the application. 

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
##########################
# example of extracting logic/verbosity
##########################
@budgets_blueprint.route("/budgets")
def budgets():

    transactions = get_transactions(request)
    transactions_sum = get_transactions_sum(transactions)
    
    budget = get_budget()
    img_src = generate_graph_img_source(transactions, budget)

    all_budgets = Budget.query.all()

    return render_template("budgets/index.jinja", budget = budget, budgets=all_budgets, transactions_sum=transactions_sum, img_src=img_src)

# we can consider doing type of refactor where ever we have a controller function with a lot of lines and logic to increase it's readability 

# we can see that this leaves our code looking more like natural language, if someone wants to see how each of these steps are done they can look into the logic inside the function. 

# this helps our controller adhear to the single responsibility principle
# this also helps us in a lot of cases to the Open/Closed principle which is one of the SOLID principles, we will look at them in slightly more detail at the course goes on. 
# I think you are the level where you will really benefit looking at them a bit earlier, here is a good article with an introduction to the topic. 
# :https://medium.com/backticks-tildes/the-s-o-l-i-d-principles-in-pictures-b34ce2f1e898


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