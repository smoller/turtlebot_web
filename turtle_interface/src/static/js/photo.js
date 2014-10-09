
$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/photo'); 

    socket.on('new photo', function(data) {
        
    });

    socket.emit('photo');

    $('#photo-button').click(function() {
        socket.emit('photo');
    }); 
});
