from app import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    comment = db.Column(db.String(255))

    def __repr__(self):
        return f"<Transaction: {self.id}: {self.amount}: {self.date}: {self.comment}>"