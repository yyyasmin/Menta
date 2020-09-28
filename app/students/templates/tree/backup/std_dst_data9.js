{% block std_dst_data9.html %}

/********** FILL DST INFO TO ALL DST TREE **************/

	var model = $(go.TreeModel);

/*****************************/
	
	var dstArray = [];
	
	window.alert( "dest" );
	window.alert( {{ dest.id }} );
	

	<!-- FROM https://stackoverflow.com/questions/41339423/how-to-fill-array-content-using-for-loop-in-javascript -->	
	[
		dstArray.push({ key: "dest.id",  name: dest.title,  dest_body: dest.body });  //DEST
	];
	
	for (var i = 1; i < {{dst_goals|length}}+1; i++) {  // GOALS
		
			[
				dstArray.push({ key: "{{ goal.id }}",  parent: "{{ dest.id }}", name: "{{ goal.title}}",  gt_body: "{{ goal.body" });
			];
			window.alert(array[i]);
	}  /***  END for (var i = 1; i < {{dst_goals|length}}+1; i++) {  to fill gol data***/

/*****************************************/	
	
	model.nodeDataArray = dstArray;

/********** FILL DST INFO TO ALL DST TREE **************/
		
{% endblock std_dst_data9.html %}
