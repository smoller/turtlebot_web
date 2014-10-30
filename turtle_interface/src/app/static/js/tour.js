var tourSocket = io.connect('http://' + document.domain + ':' + location.port + '/waypoint'); 

tour.currentWaypoint = 0;
tour.play = function() {
    
    console.log("hits");

    if (this.currentWaypoint >= this.waypoints.length) {
        return;
    }

    //Check if at correct point and move if not
    var data = {"id":this.waypoints[this.currentWaypoint].id, "position":this.waypoints[this.currentWaypoint].location};
    tourSocket.emit('move_to_waypoint', data);
    var tour = this;
    tourSocket.on('move_complete', function (data) {
        console.log(tour.currentWaypoint);
        //Stop any script playing
        window.speechSynthesis.cancel();
        //Display waypoint content
        $('#sidebar a[href="#'+tour.waypoints[tour.currentWaypoint].id+'"]').tab('show');
        //start current script
        var script = new SpeechSynthesisUtterance(); 
        script.text = tour.waypoints[tour.currentWaypoint].script;
        script.onend = function(e) {
            console.log('moving to next waypoint');
            tour.currentWaypoint++;
            tour.play();
        }
        if ('speechSynthesis' in window) {
            console.log('speech supported');
            window.speechSynthesis.speak(script); 
        } else {
            console.log('speech not supported!');
        }
    });
};

tour.stop = function() {
    window.speechSynthesis.cancel();
    tourSocket.emit('stop move');
}

tour.reset = function() {
    this.stop();
    this.currentWaypoint = 0;
    console.log(tour.currentWaypoint);
}

_.each(tour.waypoints, function(waypoint) {
    $('#sidebar').append('<li><a href="#'+waypoint.id+'" role="tab" data-toggle="pill">'+waypoint.title+'</a></li>');
    $('#content').append(function() {
        var html = '<div class="tab-pane" id="'+waypoint.id+'">';
        html += layoutContent(waypoint.content);
        html += '</div>';
        return html;
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

$('#play-button').click(function(e) {
    tour.play();
});

$('#stop-button').click(function(e) {
    tour.stop();
});

$('#restart-button').click(function(e) {
    tour.reset();
    tour.play();
});

function layoutContent(content) {

    console.log(content);
    
    var html ='<div class="row">';
    _.each(content.images, function(image) {
        html += '<div class="col-md-4">';
        html += '<a href="#" class="thumbnail">';
        html += '<img style="width:100%; height:200px;" src="'+image+'">';
        html += '</a>';
        html += '</div>';
    });
    html += '</div>';


    html += '<p>'+content.text +'</p>';
    return html;
}


annyang.debug();
annyang.addCommands({
    'play':function() {
        tour.play();
    }
});
annyang.start();
