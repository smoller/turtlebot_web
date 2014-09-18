$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/drive'); 
    Gamecontroller.init({
        left: {type: 'joystick'},
        right: {}
        touchMove: function(details) {
            socket.emit('move', {x:details.normalizedX, y:details.normalizedY});
        }
    });
});
