
$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/photo'); 
});
