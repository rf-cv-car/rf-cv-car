const { spawn } = require('child_process'), express = require('express'), ws = require('ws'),
    stream = require('stream'), http = require('http'),
    app = express(), httpServer = http.createServer(app), wsServer = new ws.Server({ server: httpServer });

let isLocked = false;

app.use('/', express.static('static'))
wsServer.on('connection', wsListener);
httpServer.listen(8080, '127.0.0.1');

function wsListener(connection) {
    if (isLocked) {
        connection.close();
        return;
    }

    isLocked = true;

    const wsStream = ws.createWebSocketStream(connection),
        cvProcess = spawn('python3', ['./cv/ball_tracking.py']),
        encodeProcess = spawn('python3', ['-u', './rf/encode_pipe.py']),
        transmitProcess = spawn('python3', ['./rf/car_transmit.py']);

    wsStream.pipe(encodeProcess.stdin);
    encodeProcess.stdout.pipe(transmitProcess.stdin);
    cvProcess.stdout.pipe(wsStream);

    function close() {
        cvProcess.kill();
        transmitProcess.kill();
        encodeProcess.kill();
        connection.close();
    }

    cvProcess.on('close', close);
    transmitProcess.on('close', close);
    encodeProcess.on('close', close);
    connection.on('close', close);
}
