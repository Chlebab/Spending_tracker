from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    transactions = db.relationship('Transaction', backref='user') 
    username = db.Column(db.String(255))
    funds = db.Column(db.Float)

    def __repr__(self):
        return f"<Transaction: {self.id}: {self.username}: {self.funds}>"