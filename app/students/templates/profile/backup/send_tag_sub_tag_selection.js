
	sub_tag_select.onchange = function(){

		sub_tag_id = sub_tag_select.value;
		console.log(sub_tag_id);
		
		fetch('/sub_tag/' + sub_tag_id);

	}
