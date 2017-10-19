from flask import Blueprint, request
from player_controller import toggle_controller 
from config import PASSPHRASE


# Register routes with webapp.py
base_routes = Blueprint('base_routes', __name__)

@base_routes.route('/toggle', methods=['POST'])
def toggle() -> tuple:
    if 'passphrase' not in request.json or request.json['passphrase'] != PASSPHRASE:
        return '', 403
    
    toggle_controller()
    return '', 204

