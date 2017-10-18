from os import listdir, sep
from random import shuffle
from pygame import init
from pygame.mixer import music
from config import MUSIC_DIR, VOLUME
IS_PAUSED = True
AUDIO_STREAM_INITED = False


def toggle_controller():
    global IS_PAUSED
    global AUDIO_STREAM_INITED

    if not AUDIO_STREAM_INITED:
        _init_audio_stream()
        AUDIO_STREAM_INITED = True

    if not IS_PAUSED:
        # Music is playing, pause it
        music.pause()
        IS_PAUSED = True
    elif IS_PAUSED and not music.get_busy():
        # We haven't started playing anything
        music.play(-1)
        IS_PAUSED = False
    elif IS_PAUSED:
        # Music is paused, resume
        music.unpause()
        IS_PAUSED = False


def _init_audio_stream():
    init()
    music.set_volume(VOLUME)

    # Get music files in dir
    music_files = [music_file for music_file in listdir(MUSIC_DIR) if music_file.endswith('.mp3')]
    shuffle(music_files)

    if len(music_files) == 0:
        raise RuntimeError('No MP3 files found in directory: {}'.format(MUSIC_DIR))

    # Load first song and queue up others
    music.load(music_files.pop(0))
    for music_file in music_files:
        music.queue(music_file)

