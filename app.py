from flask import Flask
from routes import base_routes

app = Flask(__name__)
app.register_blueprint(base_routes)
app.run(host='0.0.0.0')

