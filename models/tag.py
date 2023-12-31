from app import db

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))
    transactions = db.relationship('Transaction', backref='tag')
    activate_tag = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Tag: {self.id}: {self.category}: {self.activate_tag}>"