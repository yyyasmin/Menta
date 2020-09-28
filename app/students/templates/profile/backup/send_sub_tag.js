
	sub_tag_select.onclick = function()  {

		tag_id = tag_select.value;
		console.log("IN sub_tag_select.onchange TAG_ID:");
		console.log(tag_id);
	
		sub_tag_id = sub_tag_select.value;
		console.log("SUB_TAG_ID:");
		console.log(sub_tag_id);
		
	
	//fetch('/tag_sub_tag_to_profile_add/' + tag_id + '/' + sub_tag_id);

		var data = {
			'tag_id': tag_id,
			'sub_tag_id': sub_tag_id
			}
			
			console.log("data");
			console.log(data);
			console.log($.ajax);
			
		$.ajax({
			url: '/tag_sub_tag_to_profile_add',
			type: 'POST',
			data: data, 
			success: function(response) {
				$('body').append(response);
			}
			


		}  // END sub_tag_select.onclick 
	
	}
	
	