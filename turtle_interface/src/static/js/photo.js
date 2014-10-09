var photo_socket = io.connect('http://' + document.domain + ':' + location.port + '/photo'); 

photo_socket.on('new photo', function(data) {
    //$('#photo-panel').html('<img src=
});

photo_socket.emit('photo');

$('#photo-button').click(function(event) {
    photo_socket.emit('photo', {});
}); 
