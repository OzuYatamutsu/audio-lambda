from flask import Flask
from routes import base_routes
from config import port


app = Flask(__name__)
app.register_blueprint(base_routes)
app.run(host='0.0.0.0', port=port)

