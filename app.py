from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/spending_tracker"
db = SQLAlchemy(app)

from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction
from models.budget import Budget
from models.user import User
from models.vault import Vault

migrate = Migrate(app, db)

from controllers.transaction_controller import transactions_blueprint
from controllers.tag_controller import tags_blueprint
from controllers.merchant_controller import merchants_blueprint
from controllers.budget_controller import budgets_blueprint
from controllers.user_controller import users_blueprint
from controllers.vault_controller import vaults_blueprint

app.register_blueprint(transactions_blueprint)
app.register_blueprint(merchants_blueprint)
app.register_blueprint(tags_blueprint)
app.register_blueprint(budgets_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(vaults_blueprint)

@app.route('/', methods=["POST", "GET"])
def home():
    image_filename = 'wallet.png'  
    image_filename = 'vault.png'  
    image_filename = 'user.png'  
    image_filename = 'merchant.png'  
    image_filename = 'tag.png'  
    image_filename = 'home.png'  
    image_filename = 'budget.png'  
    image_filename = 'add.png'  
    image_filename = 'bank.png'  
    return render_template('base.jinja', image_filename=image_filename)

if __name__ == '__main__':
    app.run(debug=True)



