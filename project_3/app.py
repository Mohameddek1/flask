from flask import Flask
from config import config
from models import db, bcrypt
from routes.auth import auth_bp
from routes.customer import customer_bp
from routes.credit_card import credit_card_bp

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
bcrypt.init_app(app)

#Register blue print
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(credit_card_bp, url_prefix='/card')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)