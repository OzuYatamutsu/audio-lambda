from flask import Blueprint
from pygame import init
from pygame.mixer import music


# Register routes with webapp.py
base_routes = Blueprint('base_routes', __name__)
IS_PAUSED = True
MUSIC_FILE = '/var/ambient_audio/Matthew S Burns - Patience.mp3'

@base_routes.route('/toggle')
def toggle() -> tuple:
    global IS_PAUSED
    _init_audio_stream()

    if not IS_PAUSED:
        # Music is playing, pause it
        music.pause()
        IS_PAUSED = True
    elif IS_PAUSED and music.get_busy == 0:
        # We haven't started playing anything
        music.play(-1)
        IS_PAUSED = False
    else:
        # Music is paused, resume
        music.unpause()
        IS_PAUSED = False
    return '', 204

def _init_audio_stream():
    global MUSIC_FILE

    init()
    music.load(MUSIC_FILE)
    music.set_volume(0.4)

