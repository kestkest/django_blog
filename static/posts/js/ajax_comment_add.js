(function() {
	// adding a new form to reply to a certain comment
	$('.reply').on('click', function(e) {
		e.preventDefault();
		$('.new-form').remove();
		// get form
		var form = $('form');
		// remove newform if exists and clone the original one
		var newform = form.clone();
		newform.addClass('new-form');

		// get current comment id. 
		parent = $(this).parent().parent().parent().attr('data-value');
		// add comment's id to the newly created form
		newform.find('.parent').attr('value', parent);
		// render form under given comment
		newform.insertAfter($(this).parent().parent().parent())
		// $('.new-form').remove();
		// $(this).parent().parent().parent().parent().append(newform);
	});
	$('.container').on('click', '.add-comment', function(e) {
		e.preventDefault();
		var parent = $(this).parent();
		var parent_id = parent.find('.parent').attr('value');
		var url = parent.attr('action');
		console.log(url);
		var data = parent.serialize();
		var content = parent.find('textarea').val();
		var slug = $(this).attr('data-slug');
		// console.log(content);
		var comment_head = "<p class='comment-author'>By " + "<a href=" + data['author_url'] + "></a> @ " + data['date']  + "<span class=''>(<a href='#''>link</a>, <a  class='reply' href='#'>reply</a>)</span></p>";
		$.post(url, {'content': content, 'parent': parent_id, 'slug': slug})
			.done(function(data) {
				
    			// if (parent.attr('value')) parent.insertAfter(comment);
    			var comment_wrapper = $('[data-value=' + parent_id + ']');
    			// console.log(comment_wrapper);
    			// var container = $('.container:last');
    			// container = container[container.length - 1];
    			// var html = $.parseHTML(data);
    			$('.new-form').remove();
    			comment_wrapper.after(data);
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
