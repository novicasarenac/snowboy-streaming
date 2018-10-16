var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
    console.log('Connected...');
    recordAudio();
});

socket.on('detected', () => {
    var elem = document.createElement('h3');
    var text = document.createTextNode('Hotword detected!');
    elem.appendChild(text);
    document.body.appendChild(elem);
});

function recordAudio() {
    var session = {
        audio: true,
        video: false
    };
    navigator.mediaDevices
             .getUserMedia(session)
             .then(stream => {
                var context = new window.AudioContext();
                socket.emit('sample_rate', context.sampleRate);
                
                var audioInput = context.createMediaStreamSource(stream);
                var bufferSize = 4096;

                var recorder = context.createScriptProcessor(bufferSize, 1, 1);
                recorder.onaudioprocess = processAudio;
                
                audioInput.connect(recorder);
                recorder.connect(context.destination)
             })
             .catch(err => {
                 console.log(err);
             })
}

function processAudio(event) {
    var channelData = event.inputBuffer.getChannelData(0);

    var buffer = new ArrayBuffer(channelData.length * 2);
    var view = new DataView(buffer);
    for (var i = 0, offset = 0; i < channelData.length; i++, offset += 2) {
        var s = Math.max(-1, Math.min(1, channelData[i]));
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    socket.emit('audio', buffer);
}
