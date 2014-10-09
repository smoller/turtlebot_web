$('#sidebar').affix({
      offset: {
        top: -25 
      }
});

var $body   = $(document.body);
var navHeight = $('.navbar').outerHeight(true) + 10;

$body.scrollspy({
	target: '#left_column',
	offset: -10 
});
