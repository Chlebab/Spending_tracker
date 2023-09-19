from app import db

class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    budget_amount = db.Column(db.Integer)

    def __repr__(self):
        return f"<Budget: {self.id}: {self.budget_amount}>"