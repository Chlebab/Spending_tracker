from app import db

class Merchant(db.Model):
    __tablename__ = "merchants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    transactions = db.relationship('Transaction', backref='merchant')
    activate_merchant = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Merchant: {self.id}: {self.name}: {self.activate_merchant}>"