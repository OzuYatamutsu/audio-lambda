from os import listdir, sep
from threading import Timer
from random import shuffle
from datetime import timedelta
from pygame import init, quit
from pygame.mixer import music
from mutagen.mp3 import MP3
from config import MUSIC_DIR, VOLUME
IS_PAUSED = True
AUDIO_STREAM_INITED = False
AUDIO_LIBRARY = []
CURRENT_POS = -1
_NEXT_EVENT = None
PAUSED_POSITION = -1

def toggle_controller():
    global IS_PAUSED
    global AUDIO_STREAM_INITED
    global _NEXT_EVENT
    global PAUSED_POSITION

    if not AUDIO_STREAM_INITED:
        _init_audio_stream()
        AUDIO_STREAM_INITED = True
        IS_PAUSED = False
    elif not IS_PAUSED:
        # Music is playing, pause it
        # Save position, then stop to avoid white noise
        PAUSED_POSITION = music.get_pos()
        IS_PAUSED = True

        # Cancel the scheduled thread
        _NEXT_EVENT.cancel()

        print("Audio {} was paused ({}% played).".format( 
            _get_current_song(),
            str(_get_percent_played_for_current())
        ))

        music.stop()
        quit()

    elif IS_PAUSED:
        # Music is paused, resume
        init()
        music.set_volume(VOLUME)
        music.load(_get_current_song())
        music.play(start=PAUSED_POSITION)
        if (_get_percent_played_for_current() < 0.5):
            print("Something went wrong when trying to resume - playing next song instead.")
            play_next()
        IS_PAUSED = False

        # Resume the scheduled thread
        _resume_scheduler_for_current()
    
        print("Audio {} was resumed ({}% played).".format( 
            _get_current_song(),
            str(_get_percent_played_for_current())
        ))

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

def _resume_scheduler_for_current():
    global _NEXT_EVENT

    current_pos = music.get_pos() / 1000  # get_pos returns milliseconds
    _NEXT_EVENT = Timer(
        _get_length_of_mp3(_get_current_song()) - current_pos,
        schedule_next
    )
    _NEXT_EVENT.start()

def _get_percent_played_for_current() -> float:
    return round(
        ((music.get_pos() / 1000) / _get_length_of_mp3(_get_current_song())) * 100,
        2  # decimal places
    )

