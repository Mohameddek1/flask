from flask import Flask
from database import db, ma
from routes.init import register_blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

register_blueprint(app)

if __name__ == '__main__':
    app.run(debug=True)