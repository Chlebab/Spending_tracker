from models.transaction import Transaction
from models.budget import Budget
import matplotlib.pyplot as plt
import io
import base64


def get_transactions(request):
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if start_date and end_date:
        return Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
    else:
        return Transaction.query.all()

def get_transactions_sum(transactions):
    return sum(transaction.amount for transaction in transactions)


def get_budget():
    existing_budget = Budget.query.first()
    if existing_budget:
        return  existing_budget
    else:
        return  None
    

def generate_graph_img_source(transactions, budget):
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
    return f"data:image/png;base64,{img_base64}"

    