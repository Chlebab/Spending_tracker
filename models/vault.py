from app import db

class Vault(db.Model):
    __tablename__ = "vaults"

    id = db.Column(db.Integer, primary_key=True) 
    vault_name = db.Column(db.String(255))
    goal = db.Column(db.Float)

    def __repr__(self):
        return f"<Transaction: {self.id}: {self.vault_name}: {self.goal}>"