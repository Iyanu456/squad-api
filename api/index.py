from flask import Flask
from blueprints import user, transfer
from Models.models import StorageEngine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
storage_engine = StorageEngine('squidDB', 'localhost', 27017)


# Register Blueprints
app.register_blueprint(user.user_blueprint, url_prefix='/api/user')
app.register_blueprint(transfer.transfer_blueprint, url_prefix='/api/transfer')


if __name__ == "__main__":
    # Enable debug mode
    app.run(debug=True)
