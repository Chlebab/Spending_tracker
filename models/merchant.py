from app import db

class Merchant(db.Model):
    __tablename__ = "merchants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    transactions = db.relationship('Transaction', backref='merchant')

    def __repr__(self):
        return f"<Merchant: {self.id}: {self.name}>"