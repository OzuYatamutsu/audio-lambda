from flask import Blueprint
from config import PASSPHRASE


# Register routes with webapp.py
base_routes = Blueprint('base_routes', __name__)
IS_PAUSED = True
MUSIC_FILE = 

@base_routes.route('/toggle', method=['POST'])
def toggle() -> tuple:
    if 'passphrase' not in request.json or request.json['passphrase'] != PASSPHRASE:
        return '', 403
    
    toggle_controller()
    return '', 204

def _init_audio_stream():
    global MUSIC_FILE

    init()
    music.load(MUSIC_FILE)
    music.set_volume(0.4)

