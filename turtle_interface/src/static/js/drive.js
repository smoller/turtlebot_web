var socket = io.connect('http://' + document.domain + ':' + location.port + '/move'); 

$("#up").click(function() {
    socket.emit('move', {x:0, y:1});
});

$("#down").click(function() {
    socket.emit('move', {x:0, y:-1});
});

$("#left").click(function() {
    socket.emit('move', {x:1, y:0});
});

$("#right").click(function() {
    socket.emit('move', {x:-1, y:0});
});

var move = function(direction) {
    console.log('move cmd');
    var backwards = ['backward', 'back'];
    var forwards = ['forward', 'forwards', 'ahead', 'forth', 'on'];
    if ($.inArray(direction, forwards) > -1) {
        socket.emit('move', {x:0, y:1});
    } else if ($.inArray(direction, backwards) > -1) {
        socket.emit('move', {x:0, y:-1});
    } else {
        console.log("I don't know that direction");
    }
}

var turn = function(direction) {
    if (direction === 'left') {
        socket.emit('move', {x:1, y:0});
    } else if (direction === 'right') {
        socket.emit('move', {x:-1, y:0});
    } else {
        console.log("I don't know that direction");
    }
}

var dance = function() {
    socket.emit('move', {x:1, y:0});
    socket.emit('move', {x:0, y:1});
    socket.emit('move', {x:1, y:0});
    socket.emit('move', {x:0, y:1});
    socket.emit('move', {x:1, y:0});
    socket.emit('move', {x:0, y:1});
    socket.emit('move', {x:1, y:0});
    socket.emit('move', {x:0, y:1});
}

var voice_commands = {
    'move :direction' : move,
    'turn :direction' : turn,
    'dance' : dance
};

annyang.debug();
annyang.addCommands(voice_commands);
annyang.start();
