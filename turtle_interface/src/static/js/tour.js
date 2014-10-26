
tour.currentWaypoint = 0;
tour.executeWaypoint = function(waypoint) {

    //Check if at correct point and move if not
    //
    //Stop any script playing
    //Display waypoint content
    //start current script
    //
    //Move to next point when current script is done
    
};




var index = 0;
_.each(tour.waypoints, function(waypoint) {
    $('#sidebar').append('<li><a href="#'+index+'" role="tab" data-toggle="pill">'+waypoint.name+'</a></li>');
    $('#content').append(function() {
        var html += '<div class="tab-pane" id="'+index+'">';
        html += layoutContent(waypoint.content);
        var html = '</div>';
    });
    index++;
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
