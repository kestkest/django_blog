$(document).ready(function() {
	$('.follow').on('click', function(e){
		e.preventDefault();
		var link = $(this);
		var action;
		if (link.hasClass('add')) {
			action = 'add';
		}
		else {
			action = 'remove';
		}
		console.log(action);
		slug = $(link).attr('data-slug');
		url = $(link).attr('data-action');
		console.log(slug, url);
		$.ajax({
			url: url,
			data: {'slug': slug, 'action': action},
			method: 'POST'
		})
			.done(function(resp) {
				if (action == 'add') {
					link.removeClass('add');
					link.addClass('remove');
					link[0].innerText = 'Unfollow';
					console.log(resp);
				} else {
					link.removeClass('remove');
					link.addClass('add');
					link[0].innerText = 'Follow';
				}

			});
			
	});
});


