from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/spending_tracker"
db = SQLAlchemy(app)

from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction

migrate = Migrate(app, db)

from controllers.transaction_controller import transactions_blueprint
from controllers.tag_controller import tags_blueprint
from controllers.merchant_controller import merchants_blueprint

app.register_blueprint(transactions_blueprint)
app.register_blueprint(merchants_blueprint)
app.register_blueprint(tags_blueprint)

@app.route('/')
def home():
    return render_template('index.jinja')

if __name__ == '__main__':
    app.run(debug=True)