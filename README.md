# audio-lambda
Small RESTful API used to toggle audio playback

# Howto
### Setup your passphrase, music directory, and base volume in `config.py`...
```python
# Password included in every POST request to audio-lambda
PASSPHRASE = 'my_passphrase'

# Directory to store music files
MUSIC_DIR = '/var/music/'

# Base volume (0.0 to 1.0)
VOLUME = 0.4
```

### POST to /toggle with your passphrase
```
curl -H "Content-Type: application/json" -X POST -d '{"passphrase": "my_passphrase"}' http://localhost:5000/toggle 
```

### ♫♪♫ (=´ω｀=) ♫♪♫ 
