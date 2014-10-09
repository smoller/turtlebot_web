
$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/photo'); 

    socket.on('new photo', function(data) {
        //$('#photo-panel').html('<img src=
    });

    socket.emit('photo');

    $('#photo-button').click(function(event) {
        socket.emit('photo', {});
    }); 
});
