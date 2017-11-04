from os import listdir, sep
from threading import Timer
from random import shuffle
from datetime import timedelta
from pygame import init, quit
from pygame.mixer import music
from mutagen.mp3 import MP3
from config import MUSIC_DIR, VOLUME
IS_STOPPED = False
AUDIO_LIBRARY = []
CURRENT_POS = -1
_NEXT_EVENT = None

def toggle_controller():
    global IS_STOPPED
    global _NEXT_EVENT

    if IS_STOPPED:
        _init_audio_stream()
        IS_STOPPED = False
    else:
        # Music is playing, stop it
        music.stop()
        quit()

        # Cancel the scheduled thread for the next song
        _NEXT_EVENT.cancel()

        IS_STOPPED = True
        print("Audio {} was stopped.".format(_get_current_song()))


def play_next():
    global AUDIO_LIBRARY
    global CURRENT_POS

    CURRENT_POS = (CURRENT_POS + 1) % len(AUDIO_LIBRARY)
    print("Now playing {} ({}) - audio file {} of {}.".format(
        _get_current_song(),
        str(timedelta(seconds=_get_length_of_mp3(_get_current_song()))),
        CURRENT_POS + 1,
        len(AUDIO_LIBRARY)
    ))
    music.load(_get_current_song())
    music.play()

def schedule_next():
    global _NEXT_EVENT

    play_next()
    _NEXT_EVENT = Timer(_get_length_of_mp3(_get_current_song()), schedule_next)
    _NEXT_EVENT.start()

def _init_audio_stream():
    global AUDIO_LIBRARY

    init()
    music.set_volume(VOLUME)

    # Get music files in dir
    AUDIO_LIBRARY = [
        '{}{}{}'.format(MUSIC_DIR, sep, music_file)
        for music_file in listdir(MUSIC_DIR) if music_file.endswith('.mp3')
    ]
    shuffle(AUDIO_LIBRARY)

    if len(AUDIO_LIBRARY) == 0:
        raise RuntimeError('No MP3 files found in directory: {}'.format(MUSIC_DIR))

    # Load first song and queue up others
    schedule_next()

def _get_length_of_mp3(path: str) -> float:
    return MP3(path).info.length

def _get_current_song():
    global AUDIO_LIBRARY
    global CURRENT_POS

    return AUDIO_LIBRARY[CURRENT_POS]

