
{% block edit_std_dst_by_tag %}

<style>

table {
    font-family: arial, sans-serif;
    border-collapse: separate;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    padding: 5px;
	align: center;
}

tr:nth-child(even) {
    background-color: #dddddd;
}

table, th, td {
    border: 1px solid black;
	text-align: center;
}

#add_button  {
	-webkit-font-smoothing:subpixel-antialiased;
	background-color:#efeff5;
	margin-left: 10%;
}



</style>
	{% for tag in tags %}

		</br></br>
		<div><h4><strong>Subject: {{ tag.title }}</strong></h4></div>
		Before for dst in tag.destinations if dst in std.destinations
		{% for dst in tag.destinations if dst in std.destinations %}
			In fffffffffffff For 
			{% include "./destinations/std_edit_one_dst.html" %}
		{% endfor %}	
		
	{% endfor %}  <!-- tags -->
	</br></br>	

{% endblock %}