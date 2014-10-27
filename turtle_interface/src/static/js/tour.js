
var tourSocket = io.connect('http://' + document.domain + ':' + location.port + '/'); 

tour.currentWaypoint = 0;
tour.start = function() {

    if (this.currentWaypoint >= this.waypoints.length) {
        return;
    }

    //Check if at correct point and move if not
    var data = {"id":this.waypoints[this.currentWaypoint].id, "position":this.waypoints[this.currentWaypoint].location};
    tourSocket.emit('move to waypoint', data);
    tourSocket.on('move_complete', function (data) {
        //Stop any script playing
        window.speechSynthesis.cancel();
        //Display waypoint content
        $('#sidebar a[href="#'+this.waypoints[this.currentWaypoint].id+'"]').tab('show')
        //start current script
        var script = new SpeechSynthesisUtterance(); 
        script.text = this.waypoints[index].script;
        script.onend = function(e) {
            this.currentWaypoint++;
            this.executeFromWaypoint();
        }
        window.speechSynthesis.speak(msg); 
    } 
};

tour.stop = function() {
    window.speechSynthesis.cancel();
    //TODO stop moving
}

tour.reset = function() {
    this.stop();
    this.currentWaypoint = 0;
}

_.each(tour.waypoints, function(waypoint) {
    $('#sidebar').append('<li><a href="#'+waypoint.id+'" role="tab" data-toggle="pill">'+waypoint.name+'</a></li>');
    $('#content').append(function() {
        var html += '<div class="tab-pane" id="'+waypoint.id+'">';
        html += layoutContent(waypoint.content);
        var html = '</div>';
    });
});

//set active panes
$('#sidebar ul li:eq(0)').addClass('active');
$('#content div:eq(0)').addClass('active');

//handle clicks
$('#sidebar li a').click(function(e) {
    e.preventDefault();
    $(this).tab('show');
});

function layoutContent(content) {
    var html = '<p>'+content[0]+'</p>';
    return html;
}
