from app import app
from app import socketio
from flask import render_template, session
from ws_snowboy_decoder import WSHotwordDetector
from resampler import resample
from flask_socketio import emit


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    print('Client connected')
    session['hotword_detector'] = WSHotwordDetector('models/snowboy.umdl',
                                                     sensitivity=0.8,
                                                     audio_gain=1)


@socketio.on('sample_rate')
def client_sample_rate(sample_rate):
    print('Client\'s sample rate: {}'.format(sample_rate))
    session['sample_rate'] = sample_rate


@socketio.on('audio')
def audio(data):
    resampled_data = resample(session['sample_rate'], 16000, data)
    session['hotword_detector'].extend_buffer(resampled_data)

    if session['hotword_detector'].check_buffer():
        detected = session['hotword_detector'].perform_detection()
        if detected:
            print('Hotword detected!')
            emit('detected')
