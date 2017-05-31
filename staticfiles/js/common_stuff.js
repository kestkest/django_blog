$(document).ready(function() {
// 	$('.usr-btn').on('mouseenter', function(e) {
// 		var dropdown = $('.dropdown');
// 		// if (dropdown.css('display') == 'none') dropdown.css('display', 'block');
// 		// else dropdown.css('display', 'none');
// 		console.log(121334);
// 		dropdown.css('display', 'block');
// 	});
	

	$('.center .notification-alert').on('click', '.notify', function(e) {
		e.preventDefault();
		var ntfctns = $('.notifications');
		ntfctns.toggle();

		// send each notification id if any to mark them all as read serverside
		var count = $('#n-count');
		console.log(count.length, 'length');
		if (count.length > 0) {
			count.remove();
			var ids = [];
			var notes = $('.notification');
			for (var i = 0; i < notes.length - 1; i++) {
				var id = notes[i].childNodes[0].getAttribute("data-value");
				ids.push(id);
			}
			ids = JSON.stringify(ids);
			var mark_url = $('#notifications').attr('data-url');
			console.log(mark_url, ids);
			$.post(mark_url, {'data': ids}, function(resp) {
				console.log(resp);
			})
		}
	});
});










