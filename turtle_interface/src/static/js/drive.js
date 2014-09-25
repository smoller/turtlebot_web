$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/drive'); 
    GameController.init({
        left: {
            type: 'joystick',
            touchMove: function(details) {
                socket.emit('move', {x:details.normalizedX, y:details.normalizedY});
            }
        },
        right: {}
    });

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

    var voice_commands = {
        'move :direction' : move,
        'turn :direction' : turn,
        'dance' : dance
    }

    var move = function(direction) {
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
});
