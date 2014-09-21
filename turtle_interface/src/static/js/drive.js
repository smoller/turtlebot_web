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
});
