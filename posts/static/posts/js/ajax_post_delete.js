(function() {
	var $modal = $('.modal:first');
	var close = $('.modal-close')[0];
	var discard = $('.footer-btns .discard:first');
	var save = $('.footer-btns .save:first');
	var delete_url = $('.delete-post:first').attr('href');
	var slug = "slug=" + $('.delete-post:first').attr('data-slug');
	// var csrftoken = getCookie('csrftoken');
	// var csrftoken = $('input[type=hidden]').val();
	// console.log(save);
	var KEYCODE_ENTER = 13;
	var KEYCODE_ESC = 27;

	$(document).keyup(function(e) {
	  if (e.keyCode == KEYCODE_ENTER) $('.discard').click();
	  if (e.keyCode == KEYCODE_ESC) close_modal();
	});


	$(".delete-post").on('click', function(e) {
		e.preventDefault();
		$modal.toggle();
	});

	discard.on('click', function() {
		$.post(delete_url, {'data': slug}, function() {
			close_modal();
			window.location.replace('/posts/');
		});
	});

	var close_modal = function (e) {
			$modal.css('display', 'none');
	}

	window.onclick = function(e) {
		var modal_div = $modal[0];
		if (e.target == modal_div) close_modal();
	}
	save[0].onclick = close_modal;
	close.onclick = close_modal;
})();



