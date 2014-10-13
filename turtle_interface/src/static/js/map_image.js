var map_socket = io.connect('http://' + document.domain + ':' + location.port + '/map'); 

map_socket.on('new map', function(data) {
    $('#map-panel').html('<img src="data:image/png;base64,'+data.value+'">');
});

map_socket.emit('map');

$('#map-button').click(function(event) {
    map_socket.emit('map');
}); 
