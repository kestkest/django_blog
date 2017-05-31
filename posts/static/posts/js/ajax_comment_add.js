(function() {
	// adding a new form to reply to a certain comment
	$('#comments').on('click', '.reply', function(e) {
		e.preventDefault();
		// removing form copy if exists
		$('#copy').remove();
		comment_wrapper = $(this).parent().parent().parent().parent().parent();
		parent_id = comment_wrapper.attr('data-value');
		var newform = $('.comment-form-wrapper').clone();
		newform.find('.parent').attr('value', parent_id);
		newform.attr('id', 'copy');
		// get form
		var form = $('.comment-form-wrapper');
		// remove newform if exists and clone the original one
		// var newform = form.clone();
		newform.addClass('new-form');
		newform.insertAfter(comment_wrapper.find('.comment-right'));
		newform.find('#id_content').focus();

	});
	$('#comments').on('click', '.add-comment', function(e) {
		e.preventDefault();
		// getting two levels up to aquire form
		var form = $(this).parent().parent().find('.comment-form');
		var url = form.attr('action');
		var data = form.serialize();
		$.post(url, data)
			.done(function(resp) {
				if (resp['parent'] == 0) {
					console.log('number 0');
					var container = $('#comments');
					container.append(resp['html']);
				}
				else {
					var parent = resp['parent'];
					var comment_wrapper = $('.comment-wrapper[data-value=' + parent + "]");
					// var path = 'cid' + resp['path'].join('');
					var path = resp['path'].join('');

					console.log(path,resp['path']);
					var test = $('.comment-wrapper[data-url=cid' + path + ']');
					console.log(test);
					var index = test.length - 1;
					console.log(test[index].id, 'test');
					comment_wrapper = $('#' + test[index].id);
					// comment_wrapper = $('.comment-wrapper[id=' + test[index].id + ']');
					console.log(comment_wrapper);
					comment_wrapper.after(resp['html']);
					$('#copy').remove();
				}
				$('.empty').remove();
				$('#id_content').val('');
				console.log(resp['url'], 'url');
				$('html, body').animate({
            		scrollTop: $('.comment-wrapper[data-url^=' + resp['url'] + ']').offset().top
        		}, 300);
    			// var comment_wrapper = $('[data-value=' + parent_id + ']');
    			// $('.new-form').remove();
    			// comment_wrapper.after(data);
			});
	});


})();

function renderComment(data) {
	var wrapper = document.createElement('div');
	wrapper.classList.add('comment-wrapper');
	wrapper.style.marginLeft = data['depth'];
	wrapper.setAttribute('data-value', data['id']);
	var comment_head = document.createElement('p');
	comment_head.classList.add('comment-author');

	// var comment_head = "&ltp class='comment-author'&gtBy " + "&lta href=" + data['author_url'] + ">&lt/a&gt @ " + data['date']  + "&ltspan class=''&gt(&lta href='#''&gtlink&lt/a&gt, &lta  class='reply' href='#'&gtreply&lt/a&gt)&lt/span&gt&lt/p&gt";
	// var comment_head = "<p class='comment-author'>By " + "<a href=" + data['author_url'] + "></a> @ " + data['date']  + "<span class=''>(<a href='#''>link</a>, <a  class='reply' href='#'>reply</a>)</span></p>";
	var content = "<p>" + data['content'] + "</p>";
	wrapper.append(comment_head);
	wrapper.append(content);
	return wrapper;
}	
