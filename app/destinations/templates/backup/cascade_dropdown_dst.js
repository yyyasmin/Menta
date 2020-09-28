<script>
	vtag tag_select = document.getElementById("tag");
	vtag scrt_select = document.getElementById("scrt");

	tag_select.onchange = function()  {
		 
		tag = tag_select.value;
		
		fetch('/scrt/' + tag).then(function(response) {

			response.json().then(function(data) {
				vtag optionHTML = '';

				for (vtag scrt of data.scrts) {
					optionHTML += '<option value="' + scrt.id + '">' + scrt.title + '</option>';
				}

				scrt_select.innerHTML = optionHTML;
			})
			
		});
	}
</script>