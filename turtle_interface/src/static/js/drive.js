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
        console.log("Hits");
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
});
